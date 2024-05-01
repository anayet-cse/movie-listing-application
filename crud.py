from sqlalchemy.orm import Session
from db import models, schemas
from auth.password_hasher import *


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(email = user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_movie(db: Session, query: str):
    title = db.query(models.Movie).filter(models.Movie.title == query).order_by(models.Movie.title.asc()).all()
    if title:
        return title
    elif not title:
        cast = db.query(models.Movie).filter(models.Movie.cast == query).order_by(models.Movie.cast.asc()).all()
        if cast:
            return cast
    else: 
        return  db.query(models.Movie).filter(models.Movie.category == query).order_by(models.Movie.category.asc()).all()


def get_movie_by_title(db: Session, title: str):
    return  db.query(models.Movie).filter(models.Movie.title == title).first()


def create_favorite(db: Session, add_movie: schemas.UserFavorite):
    db_user = models.UserFavorite(title=add_movie.title, email=add_movie.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


