'''
schemas of GeoMarks
'''
import typing as tp
from pydantic import BaseModel


class GeoMarkBase(BaseModel):
    '''
    basic info of the GeoMark
    '''
    latitude: float
    longitude: float
    content: tp.Optional[str] = None


class GeoMarkCreate(GeoMarkBase):
    '''
    only base info will be needed in order to create marks

    Parameters
    ----------
    GeoMarkBase : class
        base class for GeoMark
    '''
    pass


class GeoMark(GeoMarkBase):
    '''
    additional info that we want to store

    Parameters
    ----------
    GeoMarkBase : class
        base class for GeoMark
    '''
    mark_id: int
    is_active: bool

    class Config:
        orm_mode = True
