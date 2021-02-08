from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.lib.youtube_thread import ThreadManager
from fastapi.encoders import jsonable_encoder
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

thread_manager = ThreadManager(db=deps.SessionLocal())
thread_manager.start()

@router.get("/", response_model=List[schemas.YdlItem])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """

    return crud.ydl_item.get_multi(db, skip=skip, limit=limit)

@router.get("/list")
def read_thread_items(
        db: Session = Depends(deps.get_db)
) -> List:

    return thread_manager.get_all_objects()

@router.get("/object-data/{id}")
def read_thread_items(
    id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    # import pprint
    # pprint.pprint(jsonable_encoder(db.query(models.YdlItem).all()))

    # return

    item = crud.ydl_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return thread_manager.get_object_data(item.id)

@router.post("/", response_model=schemas.YdlItem)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.YdlItemCreate,
) -> Any:
    """
    Create new item.
    """
    item = crud.ydl_item.create(db=db, obj_in=item_in)
    # if item:
        # thread_manager.add_object(item.id, item.url)
        # thread_manager.add_object(ydl_object=item)

    return item


@router.put("/{id}", response_model=schemas.YdlItem)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.YdlItemUpdate,
) -> Any:
    """
    Update an item.
    """
    item = crud.ydl_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.ydl_item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.YdlItem)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get item by ID.
    """
    item = crud.ydl_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schemas.YdlItem)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an item.
    """
    item = crud.ydl_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.ydl_item.remove(db=db, id=id)
    return item