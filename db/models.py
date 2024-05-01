from sqlalchemy import Integer, Column, String

from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    cast = Column(String)
    category = Column(String)
    release_date = Column(String)
    budget = Column(String)    

class UserFavorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    email = Column(String, unique=True)