from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
print(os.getenv("DATABASE_URL"))
DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
