import csv
from collections import OrderedDict


def get_settlements():
    with open('settlements.csv', 'r', encoding="cp1251") as f:
        csv_reader = csv.reader(f)
        settlements = OrderedDict()
        for [field] in csv_reader:
            *name, latitude, longitude = field.split(';')
            settlements[','.join(name)] = dict(
                latitude=latitude, longitude=longitude
            )
        return settlements
