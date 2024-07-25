
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controller.forms import forms
from app.controller.user import user



router = APIRouter(
    prefix='/forms',
    tags=['forms']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()


class DataForm(BaseModel):
    token: str = Field(..., min_length=1, max_length=255)
    name_form: str = Field(..., min_length=1, max_length=255)
    desc_form: str = Field(..., min_length=1, max_length=255)

class UpdateForm(BaseModel):
    id: int
    name_form: Optional[str] = None
    desc_form: Optional[str] = None
    token: str

class DeleteForm(BaseModel):
    id: int
    token: str


db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/create_form", status_code=status.HTTP_201_CREATED )
async def create_form(
    db: db_dependency,
    data_form: DataForm  
):
    user_find = await user.valid_token_user(data_form.token, db)
    user_dict = user_find['user'].get('rol')

    print(user_dict)
    if user_dict == 'client':
        response= forms.create_new_form(db, data_form)
        return response
    else:
        return {"error": "Invalid rol"}



@router.put("/update_form", status_code=status.HTTP_200_OK)
async def update_form(
    db: db_dependency,
    data_form: UpdateForm  
):
    user_find = await user.valid_token_user(data_form.token, db)
    user_dict = user_find['user'].get('rol')

    if user_dict == 'client':
        response = forms.update_form(db, data_form)
        return response
    else:
        return {"error": "Invalid rol"}
    
@router.delete("/delete_form", status_code=status.HTTP_200_OK)
async def delete_form(
    db: db_dependency,
    data_form: DeleteForm
):
    user_find = await user.valid_token_user(data_form.token, db)
    user_dict = user_find['user'].get('rol')

    if user_dict == 'client':
        response = forms.delete_form(db, data_form)
        return response
    else:
        return {"error": "Invalid rol"}