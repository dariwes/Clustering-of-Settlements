from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Settlement(Base):
    __tablename__ = 'settlements'

    id = Column(Integer, autoincrement=True, primary_key=True)
    region = Column(String, nullable=False)
    district = Column(String, nullable=False)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    population = Column(Integer, nullable=True)

    def __repr__(self):
        return (
            f'{self.region}, {self.district}, {self.name}, '
            f'latitude={self.latitude}, longitude={self.longitude}'
        )


class Duration(Base):
    __tablename__ = 'durations'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    settlement_1_id = Column(
        Integer,
        ForeignKey('settlements.id', ondelete='CASCADE'),
        nullable=False
    )
    settlement_2_id = Column(
        Integer,
        ForeignKey('settlements.id', ondelete='CASCADE'),
        nullable=False
    )
    duration = Column(Integer, nullable=False)

    def __repr__(self):
        return (
            f'{self.settlement_1_id}, {self.settlement_2_id}, {self.duration}'
        )

