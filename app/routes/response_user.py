
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controller.response_user import response_user
from app.controller.user import user

import boto3
import logging



KB = 1024
MB = 1024 * KB
SUPPORTED_FILE_TYPES = {
    'application/pdf': 'pdf',
    'image/jpeg': 'jpeg',
    'image/png': 'png',
}

AWS_BUCKET = 'sfisas'
s3 = boto3.client('s3')

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def s3_upload(contents: bytes, key: str):
    try:
        logger.info(f'Subiendo {key} a S3')
        s3.put_object(Bucket=AWS_BUCKET, Key=key, Body=contents)
    except Exception as e:
        logger.error(f'Error al subir {key} a S3: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error al subir el archivo a S3'
        )


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

class SubmitData(BaseModel):
    token: str
    id_form: int
    text: Optional[List[TextEntry]] = []
    data_file_id: List[str] = []
    data_file: List[UploadFile] = []

@router.post("/submit_data", status_code=status.HTTP_201_CREATED)
async def submit_data(
    db: Session = Depends(get_db),
    data: SubmitData = Depends()
):
    try:
        user_find = await user.valid_token_user(data.token, db)
        user_id = user_find['id']

        if data.text:
            response_user.new_response_user(db, user_id, data , data.text)

        if data.data_file:  
            responses = []
            for file in data.data_file:
                contents = await file.read()
                file_extension = SUPPORTED_FILE_TYPES.get(file.content_type)
                if not file_extension:
                    raise HTTPException(status_code=400, detail="Unsupported file type")

                key = f"{data.id_form}{user_id}_{file.filename}"
                responses.append({"filename": key})
                print(responses)
                await s3_upload(contents, key)
                
            response_user.new_response_user(db, user_id, responses, data.data_file_id)

        return {"success": True, "data": {"message": "Document update successfully."}}

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user.',
            headers={"message": f"{e}"}
        )