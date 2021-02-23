from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.lib.youtube_thread import ThreadManager
from fastapi.encoders import jsonable_encoder
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

thread_manager = ThreadManager(db=deps.SessionLocal())


# thread_manager.start()


@router.on_event("startup")
def startup():
    thread_manager.start()


@router.on_event("shutdown")
def shutdown():
    thread_manager.join()


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

@router.get("/all-thread-info")
def read_thread_info(
        db: Session = Depends(deps.get_db)
) -> List:
    return thread_manager.get_all_thread_info()

@router.get("/items-data", response_model=List[schemas.YdlItem])
def read_items_data(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,

) -> List:
    lst_result = []
    lst_items = crud.ydl_item.get_multi(db, skip=skip, limit=limit)
    if lst_items:
        for item_ in lst_items:
            dict_data_ = thread_manager.get_object_data(item_.id)
            if dict_data_:
                item_.output_log = dict_data_
            lst_result.append(item_)

    return lst_result


@router.get("/object-data/{id}")
def read_thread_items(
        id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    item = crud.ydl_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return thread_manager.get_object_data(item.id)

@router.get("/stop-thread/{id}")
def stop_thread(
        id: int,
        db: Session = Depends(deps.get_db),
) -> Any:

    is_stop = thread_manager.stop_thread_by_id(item_id=id)

    return {
        "id": id,
        'is_stop': is_stop
    }


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

    if item:
        thread_manager.remove_object(object_id=item.id)

    item = crud.ydl_item.remove(db=db, id=id)

    return item
