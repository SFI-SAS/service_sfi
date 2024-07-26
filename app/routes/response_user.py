
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controller.user import user

router = APIRouter(
    prefix='/response_user',
    tags=['response_user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TextEntry(BaseModel):
    id_question_detail_form: int
    response: Optional[str] = None

class FileEntry(BaseModel):
    id_question_detail_form: int
    response: Optional[str] = None

class SubmitData(BaseModel):
    token: str
    id_form: int
    text: Optional[List[TextEntry]] = []
    file: Optional[List[FileEntry]] = []

@router.post("/submit_data", status_code=status.HTTP_201_CREATED)
async def submit_data(
    db: db_dependency,
    data: SubmitData
):
    user_find = await user.valid_token_user(data.token, db)
    user_id = user_find['id']

    if data.text:
        print("lleagron datos  data text",user_id)

    if data.file:
       print("lleagron datos ",user_id)

    return {"message": "Data submitted successfully"}