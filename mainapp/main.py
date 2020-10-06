'''
main back-end file, API
'''
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import typing as tp

from sqlalchemy.orm import Session

from . import crud, models, schemas
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine

app = FastAPI()
app.mount('/static', StaticFiles(directory='./static'), name='static')
templates = Jinja2Templates(directory="./templates")

models.Base.metadata.create_all(bind=engine)

# solving CORS problem
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', response_class=HTMLResponse)
def render_front(request: Request):
    return templates.TemplateResponse('map.html', {'request': request})


@app.post('/create_mark/', response_model=schemas.GeoMark)
def create_mark(mark: schemas.GeoMarkCreate, db: Session = Depends(get_db)):
    '''
    create mark

    Parameters
    ----------
    mark : schemas.GeoMarkCreate
        base GeoMark info:
            latitude,
            longitude,
            content
    db : Session, optional
        by default Depends(get_db)

    Returns
    -------
    models.GeoMark
        inserted GeoMark

    Raises
    ------
    HTTPException
        Mark with the given latitude, longitude already exists
    '''
    db_mark = crud.get_mark_by_latlong(db,
                                       latitude=mark.latitude,
                                       longitude=mark.longitude)
    if db_mark:
        raise HTTPException(status_code=400,
                            detail='Mark with the given latitude, longitude already exists')
    return crud.create_mark(db=db, mark=mark)


@app.get('/marks/', response_model=tp.List[schemas.GeoMark])
def read_marks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    get limit of marks

    Parameters
    ----------
    skip : int, optional
        amount of marks, by default 0
    limit : int, optional
        limit to be given, by default 100
    db : Session, optional
        by default Depends(get_db)
    '''
    marks = crud.get_marks(db, skip=skip, limit=limit)
    return marks


@app.post('/make_mark_inactive/', response_model=schemas.GeoMark)
def make_mark_inactive(mark_id: int, db: Session = Depends(get_db)):
    '''
    set mark's status to inactive by mark_id

    Parameters
    ----------
    mark_id : int
        id
    db : Session, optional
        by default Depends(get_db)

    Returns
    -------
    updated mark on success

    Raises
    ------
    HTTPException
        Mark with the given id is not found
    '''
    db_mark = crud.delete_mark_by_id(db, mark_id=mark_id)
    if not db_mark:
        raise HTTPException(status_code=400,
                            detail='Mark with the given id is not found')
    return db_mark


@app.post('/make_mark_active/', response_model=schemas.GeoMark)
def make_mark_active(mark_id: int, db: Session = Depends(get_db)):
    '''
    set mark's status to active by id

    Parameters
    ----------
    mark_id : int
        id
    db : Session, optional
        by default Depends(get_db)

    Returns
    -------
    updated mark on success

    Raises
    ------
    HTTPException
        Mark with the given id is not found
    '''
    db_mark = crud.make_mark_as_active_by_id(db, mark_id=mark_id)
    if not db_mark:
        raise HTTPException(status_code=400,
                            detail='Mark with the given id is not found')
    return db_mark
