
import datetime
import os
import random
from fastapi import HTTPException, Depends
from starlette import status
from typing import Annotated
from app.models import QuestionDetailForm, QuestionsDetail, ResponseUser


class response_user():       

    def new_response_user(db,user_id, data):

        for text_entry in data.text:
            question_detail_form = db.query(QuestionDetailForm).filter(QuestionDetailForm.id == text_entry.id_question_detail_form).first()
            if question_detail_form:
                new_response = ResponseUser(
                    id_question_detail_form=text_entry.id_question_detail_form,
                    id_form=data.id_form,
                    id_user=user_id,
                    response=text_entry.response
                )
                db.add(new_response)
            else:
                raise HTTPException(status_code=404, detail=f"QuestionDetailForm with ID {text_entry.id_question_detail_form} not found")
        db.commit()
    
    async def generate_unique_filename(original_filename: str) -> str:

        ext = os.path.splitext(original_filename)[1]
    
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S%f')

        random_numbers = random.randint(1000, 9999)
        
        # Combinar la fecha y hora actual con el nombre original y la extensión
        new_filename = f"{current_datetime}_{random_numbers}.pdf"
        
        return new_filename
    