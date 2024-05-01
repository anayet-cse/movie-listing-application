from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:anayet007@localhost:5432/bpdb"
#"postgresql://user:password@postgresserver/db"
# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#declarative_base() that returns a class.
#inherit from this class to create each of the database models or classes (the ORM models)
Base = declarative_base()