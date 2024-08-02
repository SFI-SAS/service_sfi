from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD_BD = os.getenv("PASSWORD_DB")
USER_BD = os.getenv("USER_DB")
HOST_BD = os.getenv("HOST_DB")


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{USER_BD}:{PASSWORD_BD}@{HOST_BD}:3306/forms_sfi'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=2, pool_timeout=30, pool_recycle=1800)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()