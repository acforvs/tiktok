'''
database table models
'''
from sqlalchemy import Boolean, Column, Integer, String, Float

from .database import Base


class GeoMark(Base):
    '''
    basic class for GeoMark, represents GeoMark instance in the database

    Parameters
    ----------
    Base
        Base database class
    '''
    __tablename__ = 'marks'

    mark_id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)

    content = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
