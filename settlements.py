import csv
from collections import OrderedDict
from db_manager import DatabaseManager
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
