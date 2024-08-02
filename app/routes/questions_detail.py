
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controller.questions_detail import questions_detail
from app.controller.user import user


router = APIRouter(
    prefix='/questions_detail',
    tags=['questions_detail']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class Data(BaseModel):
    name_label: str
    type: str
    status: str
    position: int

class DataQuestion(BaseModel):
    id_form: int
    token: str
    data: List[Data]


class UpdateQuestion(BaseModel):
    id: int
    name_label:  Optional[str] = None
    type:  Optional[str] = None
    status:  Optional[str] = None
    position:  Optional[str] = None
    token: str

class DeleteQuestion(BaseModel):
    id: int
    token: str


@router.post("/create_questions", status_code=status.HTTP_201_CREATED )
async def create_form(
    db: db_dependency,
    data_question: DataQuestion  
):
    user_find = await user.valid_token_user(data_question.token, db)
    user_dict = user_find['user'].get('rol')

    if user_dict == 'client':
        response= questions_detail.new_questions_detail(db, data_question)
        return response
    else:
        return {"error": "Invalid rol"}
    

@router.put("/update_questions", status_code=status.HTTP_200_OK)
async def update_questions(
    db: db_dependency,
    data_question: UpdateQuestion  
):
    user_find = await user.valid_token_user(data_question.token, db)
    user_dict = user_find['user'].get('rol')

    if user_dict == 'client':
        response = questions_detail.update_question(db, data_question)
        return response
    else:
        return {"error": "Invalid rol"}
    

@router.delete("/delete_questions", status_code=status.HTTP_200_OK)
async def delete_questions(
    db: db_dependency,
    data_question: DeleteQuestion
):
    user_find = await user.valid_token_user(data_question.token, db)
    user_dict = user_find['user'].get('rol')

    if user_dict == 'client':
        response = questions_detail.delete_question(db, data_question)
        return response
    else:
        return {"error": "Invalid rol"}