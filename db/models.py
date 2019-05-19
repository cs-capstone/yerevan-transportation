from sqlalchemy import Column, Integer, String, Numeric, types, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Base(object):
    def __json__(self, request):
        json_exclude = getattr(self, '__json_exclude__', set())
        return {key: str(value) for key, value in self.__dict__.items()
                # Do not serialize 'private' attributes
                # (SQLAlchemy-internal attributes are among those, too)
                if not key.startswith('_')
                and key not in json_exclude}


Base = declarative_base(cls=Base)


class TransportType(object):
    BUS = 'bus'
    MICROBUS = 'microbus'
    METRO = 'metro'

    @classmethod
    def get_transport_type_array(cls):
        return [cls.BUS, cls.MICROBUS, cls.METRO]


connected_stations = Table('connected_stations', Base.metadata,
                           Column('first_station_id', Integer, ForeignKey('station.id')),
                           Column('second_station_id', Integer, ForeignKey('station.id'))
                           )

transport_station = Table('transport_station', Base.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('station_id', Integer, ForeignKey('station.id')),
                          Column('transport_id', Integer, ForeignKey('transport.id'))
                          )


class Transport(Base):
    __tablename__ = 'transport'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(types.Enum(*TransportType.get_transport_type_array(), name='transport_type'), nullable=False)


class Street(Base):
    __tablename__ = 'street'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Station(Base):
    __tablename__ = 'station'
    __json_exclude__ = ['neighbor_stations', 'transports']
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    street_id = Column(Integer, ForeignKey('street.id'))
    lng = Column(Numeric)
    lat = Column(Numeric)
    neighbor_stations = relationship('Station',
                                     secondary=connected_stations,
                                     primaryjoin=id == connected_stations.c.first_station_id,
                                     secondaryjoin=id == connected_stations.c.second_station_id
                                     )
    transports = relationship('Transport', secondary=transport_station, backref='stations')

    street = relationship(Street)
