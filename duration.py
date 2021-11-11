import asyncio
from pprint import pprint
from settlements import get_settlements
import aiohttp


async def get_duration(session, url, first_settlement, second_settlement):
    async with session.get(url) as response:
        data = await response.json()
        pprint(data)
        if response.status == 200:
            return (
                first_settlement,
                second_settlement,
                data['routes'][0].get('duration')
            )


async def get_durations():
    url = (
        'https://api.mapbox.com/directions/v5/'
        'mapbox/driving/{};{}?access_token={}'
    )
    settlements = get_settlements()
    token = (
        'pk.eyJ1IjoiZGFyaXdlcyIsImEiOiJja3ZndmQ4bjYyN'
        'mU4MzFwZ2xsZms2djh0In0.W1hVnAwsVmyMKOZ33moE6Q'
    )
    async with aiohttp.ClientSession() as session:
        tasks = []
        while settlements:
            first_name, first_coordinates = settlements.popitem(last=False)
            for second_name, second_coordinates in settlements.items():
                tasks.append(asyncio.ensure_future(
                    get_duration(
                        session, url.format(
                            ','.join(first_coordinates.values()),
                            ','.join(second_coordinates.values()),
                            token
                        ),
                        {first_name: first_coordinates},
                        {first_name: first_coordinates}
                    )
                ))
        result = await asyncio.gather(*tasks)
        return result


def get_data():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_durations())
    loop.run_until_complete(future)
    print(future.result())


if __name__ == '__main__':
    get_data()
