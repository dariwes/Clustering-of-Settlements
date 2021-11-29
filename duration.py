import asyncio
import aiohttp
from settlements import get_all_coordinates


URL = (
    'https://api.mapbox.com/'
    'directions/v5/mapbox/driving/{};{}?access_token={}'
)
TOKEN = 'TODO: your token'
TASKS_SIZE = 1000
QUEUE_SIZE = 1500


async def get_duration(session, url, first_id, second_id):
    async with session.get(url) as response:
        data = await asyncio.wait_for(response.json(), timeout=5.0)
        if response.status == 200:
            try:
                return first_id, second_id, data['routes'][0]['duration']
            except IndexError or KeyError:
                return None


async def fetch_duration(queue, durations):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                data = await queue.get()
                if not data:
                    return None
                (
                    (first_id, first_coordinates),
                    (second_id, second_coordinates)
                ) = data
                response = await get_duration(
                    session, URL.format(
                        '{},{}'.format(*first_coordinates.values()),
                        '{},{}'.format(*second_coordinates.values()),
                        TOKEN
                    ),
                    first_id,
                    second_id
                )
                if response:
                    durations.append(response)
            finally:
                queue.task_done()


async def fetch_durations():
    queue = asyncio.Queue(maxsize=QUEUE_SIZE)
    coordinates = get_all_coordinates()
    tasks = []
    durations = []
    for _ in range(TASKS_SIZE):
        tasks.append(asyncio.create_task(fetch_duration(queue, durations)))
    while coordinates:
        first_coordinates = coordinates.popitem(last=False)
        for second_coordinates in coordinates.items():
            await queue.put((first_coordinates, second_coordinates))
    for _ in range(TASKS_SIZE):
        await queue.put(None)
    await queue.join()
    await asyncio.gather(*tasks)
    return durations


def get_durations():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_durations())
    loop.run_until_complete(future)
    return future.result()
