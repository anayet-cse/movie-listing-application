from pydantic import BaseModel

class UserBase(BaseModel):
    email : str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    class Config:
        orm_mode = True

class UserDetails(BaseModel):
    email: str
    user_id: int

class APIResponseModel(User):
    statuscode : int
    class Config:
        orm_mode = True

class Movie(BaseModel):
    id: int
    title: str
    cast: list[str]
    category: str
    release_date: str
    budget: float

class UserFavorite(BaseModel):
    id: str
    title: str
    email: str

class Message(BaseModel):
    message: str


class UserDetailsOut(UserBase):
    email: str
    favorite: list[UserFavorite]

class UserFavoriteOut(BaseModel):
    title: str