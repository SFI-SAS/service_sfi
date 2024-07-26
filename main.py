import app.models as models
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.config import database
from app.routes import auth, forms, questions_detail, response_user


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally: 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth.router)
app.include_router(forms.router)
app.include_router(questions_detail.router)
app.include_router(response_user.router)