
from fastapi import APIRouter

from app.config.database import SessionLocal


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
        