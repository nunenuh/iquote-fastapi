from .crud_author import author
from .crud_categories import categories
from .crud_quote import quote
from .crud_user import user

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from models.item import Item
# from schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
# from .crud_item import item
