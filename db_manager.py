from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased
from models import Settlement, Duration, Base


class DatabaseManager:
    def __init__(self, dbname, user, password, host):
        self.engine = create_engine(
            f'postgresql://{user}:{password}@{host}/{dbname}'
        )
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def insert_settlements(self, settlements):
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

    def insert_durations(self, durations):
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

    def get_all_coordinates(self):
        session = self.Session()
        return session.query(
            Settlement.id, Settlement.latitude, Settlement.longitude
        ).all()

    def get_all_durations(self):
        session = self.Session()
        return session.query(
            Duration.settlement_1_id,
            Duration.settlement_2_id,
            Duration.duration
        ).all()

    def get_certain_durations(self, min_duration, max_duration):
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

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
