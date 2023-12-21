from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

# This Config class is used to provide configurations to Pydantic.
    class Config:
        # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model
        orm_mode = True
# Technical Details about ORM mode
# SQLAlchemy and many others are by default "lazy loading".
# That means, for example, that they don't fetch the data for relationships from the
# database unless you try to access the attribute that would contain that data.


class UserBase(BaseModel):
    email: str


# have a password when creating it.
class UserCreate(UserBase):
    password: str


# But for security, the password won't be in other Pydantic models
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
