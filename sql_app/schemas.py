from pydantic import BaseModel

class ItemEntry(BaseModel):
    name: str
    price: float
    date: str

class Item(BaseModel):
    id: int
    name: str
    price: float
    date: str

    class Config:
        orm_mode = True