
import json
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
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



class TextItem(BaseModel):
    id_question_detail_form: str
    response: str

@router.post("/submit_data", status_code=status.HTTP_201_CREATED)
async def test_endpoint(
    db: db_dependency, 
    token: str = Form(...),
    id_form: int = Form(...),
    text: Optional[str] = Form(None), 
    data_file_id: List[str] = Form(...),
    data_file: List[UploadFile] = File(...),  
):
    user_find = await user.valid_token_user(token, db)
    user_id = user_find['id']

    if text:
        try:
            text_items = json.loads(text)
            text_data = [TextItem(**item) for item in text_items]
            print(text, text_data)
            response_user.new_response_user(db, user_id, id_form, text_data)
        except (json.JSONDecodeError, TypeError) as e:
            raise HTTPException(status_code=400, detail="Invalid text format")
    else:
        text_data = []  

    if data_file and data_file_id:
            responses = []
            for file in data_file:
                try:
                    contents = await file.read()
                    file_extension = SUPPORTED_FILE_TYPES.get(file.content_type)
                    if not file_extension:
                        raise HTTPException(status_code=400, detail="Unsupported file type")
                    key = f"{id_form}_{user_id}_{file.filename}"
                    await s3_upload(contents, key)
                    responses.append({"filename": key})

                    
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")
                
            result_json = {
            "files": [
                {"id_question_detail_form": fid, "response": resp["filename"]}
                for fid, resp in zip(data_file_id, responses)
            ]
            }
            print(f"Sending result_json: {result_json}")
            response_user.new_response_user(db, user_id, id_form, result_json['files'])
    return {"success": True, "data": {"message": "Documents updated successfully."}}