import csv
import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Settlement, Duration, Base


class DatabaseManager:
    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.engine = create_engine(
            f'postgresql://{user}:{password}@{host}/{dbname}'
        )
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def insert_settlements(self, settlements: typing.List[tuple]):
        session = self.Session()
        db_data = list()
        for region, district, name, latitude, longitude in settlements:
            db_data.append(
                Settlement(
                    region=region, district=district, name=name,
                    latitude=latitude, longitude=longitude
                )
            )
        session.add_all(db_data)
        session.commit()

    def insert_durations(self, durations: typing.List[tuple]):
        session = self.Session()
        db_data = list()
        for settlement_1_id, settlement_2_id, duration in durations:
            db_data.append(
                Duration(
                    settlement_1_id=settlement_1_id,
                    settlement_2_id=settlement_2_id,
                    duration=duration
                )
            )
        session.add_all(db_data)
        session.commit()

    def insert_population(self, data: typing.List[tuple]):
        session = self.Session()
        for id, population in data:
            session.query(Settlement).filter(Settlement.id == id).update(
                {Settlement.population: population}, synchronize_session=False
            )
        session.commit()

    def get_all_coordinates(self) -> list:
        session = self.Session()
        return session.query(
            Settlement.id, Settlement.latitude, Settlement.longitude
        ).all()

    def get_names(self) -> list:
        session = self.Session()
        return session.query(
            Settlement.id, Settlement.name
        ).all()

    def get_all_durations(self) -> list:
        session = self.Session()
        return session.query(
            Duration.settlement_1_id,
            Duration.settlement_2_id,
            Duration.duration
        ).all()

    def get_certain_durations(
            self, min_duration: int, max_duration: int
    ) -> list:
        session = self.Session()
        return session.query(
            Settlement.name,
            Settlement.latitude,
            Settlement.longitude,
        ).join(
            Duration,
            Duration.settlement_1_id == Settlement.id or
            Duration.settlement_2_id == Settlement.id
        ).filter(
            Duration.duration > min_duration,
            Duration.duration <= max_duration
        ).distinct().all()

    def write_csv_durations(self):
        durations = list(self.get_all_durations())
        with open('durations.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(durations)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
