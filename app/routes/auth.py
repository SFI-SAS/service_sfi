from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controller.user import user


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
    
class UserRegister(BaseModel):
    num_document: str = Field(..., min_length=1, max_length=255)
    full_name: str = Field(..., min_length=1, max_length=255)
    telephone: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=255)
    rol: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=120)

class Token(BaseModel):
    access_token: str
    token_type: str

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code=status.HTTP_201_CREATED )
async def register_user(
    db: db_dependency,
    user_register: UserRegister  
):
    try:
        creation_result = user.register_new_user(db, user_register)
        return creation_result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.', headers={"message": f"{e}"})

@router.post("/get_token", response_model=Token)
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: db_dependency):
    response = await user.login_access(form_data, db)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.post("/valid_token")
async def valid_token(token: Token, db: db_dependency):
    user_find = await user.valid_token_user(token.access_token, db)
    
    if user_find != None:
        return {"status": True, "user": user_find["user"] }
    else:
        return {"status": False, "user": None}
    