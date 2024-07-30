
from datetime import datetime, timedelta
import os
import random
from fastapi import HTTPException, Depends
from starlette import status
from typing import Annotated
from app.models import QuestionDetailForm, QuestionsDetail, ResponseUser


class response_user():       

    def new_response_user(db,user_id,id_form, data):

        for text_entry in data:
            question_detail_form = db.query(QuestionDetailForm).filter(QuestionDetailForm.id == text_entry.id_question_detail_form).first()
            if question_detail_form:
                new_response = ResponseUser(
                    id_question_detail_form=text_entry.id_question_detail_form,
                    id_form=id_form,
                    id_user=user_id,
                    response=text_entry.response
                )
                db.add(new_response)
            else:
                raise HTTPException(status_code=404, detail=f"QuestionDetailForm with ID {text_entry.id_question_detail_form} not found")
        db.commit()
