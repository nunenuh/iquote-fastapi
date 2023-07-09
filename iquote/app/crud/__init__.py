from .crud_item import item
from .crud_quote import quote
from .crud_quote_author import quote_author
from .crud_quote_categories import quote_categories
from .crud_user import user

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from models.item import Item
# from schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
