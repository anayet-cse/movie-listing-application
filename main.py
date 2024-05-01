from fastapi import Depends, FastAPI, HTTPException
from db.database import engine
from sqlalchemy.orm import Session
import crud
from db import schemas
from db.database import SessionLocal
from db import models
from auth import password_hasher

#Create all the database tables defined in the SQLAlchemy models and bind them to the specified database engine
models.Base.metadata.create_all(bind=engine)

# Create a new FastAPI application instance
app =  FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define a route using the app instance
@app.post("/user/signup", response_model = schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
            raise HTTPException(status_code=400, detail="userName already registered")
    return crud.create_user(db = db, user = user)
    

# Login Routes
@app.post("/user/login")
def user_login(email : str, password : str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    isMatched = password_hasher.verify_password(password, db_user.password)
    
    if (db_user and isMatched):
        raise HTTPException(status_code=200, detail="OK")
    raise HTTPException(status_code=401, detail="Wrong credentials details!")


# Search movies by title, cast, or category
@app.get("/movies/{query}")
def search_movies(query: str, db: Session = Depends(get_db)):
    user_movies = crud.get_movie(db, query=query)
    return user_movies


# Get details of a specific movie
@app.get("/movies/{title}/", response_model = schemas.Movie)
def get_movie_details(title: str, db: Session = Depends(get_db)):
    user_movies = crud.get_movie_by_title(db, title=title)

    if user_movies:
        raise HTTPException(status_code=404, detail="Movie not found")
    return user_movies


# Add a movie to favorites
@app.patch("/favorites/add/{movie_title}", response_model=schemas.Message)
def add_to_favorites(email: str, movie_title: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    movie_title = crud.get_movie_by_title(title=movie_title)
    if movie_title is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    add_movie = schemas.UserFavorite(title=movie_title, email=email)
    add_movie = crud.create_favorite(add_movie=add_movie)
    return schemas.Message(message="Update successfully")


# Remove a movie from favorites
@app.patch("/favorites/remove/", response_model=schemas.Message)
def remove_from_favorites(email: str, movie_title: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    movie_title = crud.get_movie_by_title(db, title=movie_title)
    if movie_title is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(movie_title)
    db.commit()
    return schemas.Message(message="Delete successfully")


# User details and their favorite movies
@app.get("/user/{email}/")
def get_user_details(email: str):
    return 


# Search only movies added to favorites
@app.get("/favorites/{email}/")
def search_favorites(email: str):
    return