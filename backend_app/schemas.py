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


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    username: str
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str
    item_id: int


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    user_id: int
    created_date: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
