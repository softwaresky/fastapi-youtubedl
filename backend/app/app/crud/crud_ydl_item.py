from typing import List
from app.models.ydl_item import YdlItem
from app.schemas.ydl_item import YdlItemCreate, YdlItemUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

class CRUDYdlItem(CRUDBase[YdlItem, YdlItemCreate, YdlItemUpdate]):

    def get_multi_by_status(self, db: Session, status = 0) -> List[YdlItem]:
        return db.query(self.model).filter(self.model.status == status if status else True).all()

ydl_item = CRUDYdlItem(YdlItem)