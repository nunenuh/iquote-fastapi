from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.quote import Categories
from schemas.categories import CategoriesCreate, CategoriesUpdate


class CRUDCategories(CRUDBase[Categories, CategoriesCreate, CategoriesUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Categories]:
        return db.query(Categories).filter(Categories.name == name).first()

    def get_by_parent_id(self, db: Session, *, parent_id: int) -> List[Categories]:
        return db.query(Categories).filter(Categories.parent_id == parent_id).all()

    def get_by_parent_name(self, db: Session, *, parent_name: str) -> List[Categories]:
        return (
            db.query(Categories)
            .join(Categories.parent)
            .filter(Categories.parent.has(name=parent_name))
            .all()
        )

    def create_by_parent(
        self, db: Session, parent_id: int, obj_in: CategoriesCreate
    ) -> Categories:
        db_obj = Categories(**obj_in.dict(), parent_id=parent_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(self, db: Session, *, obj_in: CategoriesCreate) -> Categories:
        db_obj = Categories(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Categories,
        obj_in: Union[CategoriesUpdate, Dict[str, Any]]
    ) -> Categories:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


categories = CRUDCategories(Categories)
