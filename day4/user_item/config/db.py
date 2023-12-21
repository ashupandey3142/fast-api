from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/test"
# This line creates a SQLAlchemy database engine using the provided database URL. The engine is responsible for managing database connections.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Declarative classes are used to define database tables and their schema.
Base = declarative_base()
