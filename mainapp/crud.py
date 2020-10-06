'''
funcs to work with a database
'''
from sqlalchemy.orm import Session
import typing as tp
from . import models, schemas


def create_mark(db: Session, mark: schemas.GeoMarkCreate) -> models.GeoMark:
    '''
    insert mark data into the database

    Parameters
    ----------
    db : Session
        current session
    mark : schemas.GeoMarkCreate
        mark to be inserted

    Returns
    -------
    models.GeoMark
        inserted mark on success
        includes mark_id & is_active (default true)
    '''
    db_mark = models.GeoMark(latitude=mark.latitude,
                             longitude=mark.longitude,
                             content=mark.content)
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark


def get_marks(db: Session, skip: int = 0, limit: int = 100) -> tp.List[models.GeoMark]:
    '''
    get [limit] marks from the database with offset [skip]

    Parameters
    ----------
    db : Session
        current session
    skip : int, optional
        amount of marks to be skipped, by default 0
    limit : int, optional
        amount of marks to be returned, by default 100

    Returns
    -------
    tp.List[models.GeoMark]

    '''
    return db.query(models.GeoMark).offset(skip).limit(limit).all()


def delete_mark_by_id(db: Session, mark_id: int) -> tp.Optional[models.GeoMark]:
    '''
    set status to inactive bu mark_id

    Parameters
    ----------
    db : Session
        current session
    mark_id : int
        id

    Returns
    -------
    tp.Optional[models.GeoMark]
        updated mark on success, None otherwise
    '''
    db_mark = db.query(models.GeoMark).filter(models.GeoMark.mark_id == mark_id).first()
    try:
        db_mark.is_active = False
        db.commit()
        return db_mark
    except:
        return None


def make_mark_as_active_by_id(db: Session, mark_id: int) -> tp.Optional[models.GeoMark]:
    '''
    update mark is_activs status and set it to active

    Parameters
    ----------
    db : Session
        current session
    mark_id : int
        id

    Returns
    -------
    tp.Optional[models.GeoMark]
        models.GeoMark on success, None otherwise
    '''
    db_mark = db.query(models.GeoMark).filter(models.GeoMark.mark_id == mark_id).first()
    try:
        db_mark.is_active = True
        db.commit()
        return db_mark
    except:
        return None


def get_mark_by_latlong(db: Session, latitude: float, longitude: float) -> models.GeoMark:
    '''
    get mark info by latitude, longitude

    Parameters
    ----------
    db : Session
        current session
    latitude : float
        latitude
    longitude : float
        longitude

    Returns
    -------
    models.GeoMark
        geomark with the given parameters
    '''
    return db.query(models.GeoMark).filter(models.GeoMark.latitude == latitude,
                                           models.GeoMark.longitude == longitude).first()
