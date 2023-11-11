from pydantic import BaseModel
from datetime import date


class ItemEntry(BaseModel):
    name: str
    price: float
    date: str


class PriceBase(BaseModel):
    pass


class PriceEntry(PriceBase):
    item_id: int
    price: float
    date: str


class Price(PriceEntry):
    id: int

    class Config:
        orm_mode = True


class Item(BaseModel):
    id: int
    name: str
    prices: list[Price]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    username: str
    id: int
    is_active: bool
    role: str
    is_subscribed: bool

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str
    item_id: int


class CommentForm(CommentBase):
    pass


class CommentCreate(CommentForm):
    user_id: int


class Comment(CommentBase):
    id: int
    user_id: int
    created_date: str

    class Config:
        orm_mode = True


class ItemFollowers(BaseModel):
    item_id: int
    user_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class FollowRequest(BaseModel):
    item_id: int
    

class SubscriptionCreate(BaseModel):
    start_date: date
    end_date: date
    user_id: int

class SubscriptionRequest(BaseModel):
    months: int

class Subscription(SubscriptionCreate):
    id: int

class SignupResponse(BaseModel):
    user: User
    token: str
