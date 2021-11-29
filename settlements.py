import asyncio
import csv
import re
import typing
import aiohttp
from collections import OrderedDict
from bs4 import BeautifulSoup
from database.db_manager import DatabaseManager
from config import db_settings


def get_all_coordinates():
    db_manager = DatabaseManager(**db_settings)
    return OrderedDict(
        (settlement_id, {'latitude': latitude, 'longitude': longitude})
        for settlement_id, latitude, longitude in
        db_manager.get_all_coordinates()
    )


def fill_database():
    with open('settlements.csv', 'r', encoding="cp1251") as csv_file:
        csv_reader = csv.reader(csv_file)
        settlements = list()
        for [field] in csv_reader:
            settlements.append(field.split(';'))
    db_manager = DatabaseManager(**db_settings)
    db_manager.create_tables()
    db_manager.insert_settlements(settlements)


async def get_population(session, url, settlement_id):
    async with session.get(url) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'lxml')
        data = soup.find(
            attrs={'class': 'no-wikidata', 'data-wikidata-property-id': 'P1082'}
        )
        if data:
            population = re.search('>([0-9 ]+)<', ''.join(str(data)))
            if population:
                population = population.group(1).replace(' ', '')
                print(population)
                return settlement_id, int(population) if population else None


async def get_population_list(names: typing.List[tuple]) -> typing.List[tuple]:
    DOMAIN_NAME = 'https://ru.wikipedia.org/wiki/'
    async with aiohttp.ClientSession() as session:
        tasks = []
        for id, name in names:
            url = DOMAIN_NAME + name
            tasks.append(asyncio.ensure_future(
                get_population(session, url, id)
            ))
        population = await asyncio.gather(*tasks)
        return list(filter(None, population))


def fill_population():
    db_manager = DatabaseManager(**db_settings)
    names = db_manager.get_names()
    population = asyncio.run(get_population_list(names))
    db_manager.insert_population(population)
