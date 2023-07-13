from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()

    def get_by_parent_id(self, db: Session, *, parent_id: int) -> List[Category]:
        return db.query(Category).filter(Category.parent_id == parent_id).all()

    def get_by_parent_name(self, db: Session, *, parent_name: str) -> List[Category]:
        return (
            db.query(Category)
            .join(Category.parent)
            .filter(Category.parent.has(name=parent_name))
            .all()
        )

    def create_by_parent(
        self, db: Session, parent_id: int, obj_in: CategoryCreate
    ) -> Category:
        db_obj = Category(**obj_in.model_dump(), parent_id=parent_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        db_obj = Category(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Category,
        obj_in: Union[CategoryUpdate, Dict[str, Any]]
    ) -> Category:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


categories = CRUDCategory(Category)
