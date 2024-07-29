
import datetime
import os
import random
from fastapi import HTTPException, Depends
from starlette import status
from typing import Annotated
from app.models import QuestionDetailForm, QuestionsDetail, ResponseUser


class response_user():       

    def new_response_user(db, user_id, id_form, text):
        if not isinstance(text, list):
            raise HTTPException(status_code=400, detail="Expected a list of entries")
        
        print(f"Received entries: {text}")
        
        for index, text_entry in enumerate(text):
            if not isinstance(text_entry, dict):
                raise HTTPException(status_code=400, detail="Each entry should be a dictionary")
            
            ids_question_detail_form = text_entry.get("id_question_detail_form")
            response = text_entry.get("response")
            
            # Dividir los IDs si hay varios
            ids_list = ids_question_detail_form.split(',')
            print(f"Processing entry {index + 1}: ids_question_detail_form={ids_list}, response={response}")

            for id_question_detail_form in ids_list:
                id_question_detail_form = id_question_detail_form.strip()  # Eliminar espacios en blanco
                
                question_detail_form = db.query(QuestionDetailForm).filter(QuestionDetailForm.id == id_question_detail_form).first()
                if question_detail_form:
                    new_response = ResponseUser(
                        id_question_detail_form=id_question_detail_form,
                        id_form=id_form,
                        id_user=user_id,
                        response=response
                    )
                    db.add(new_response)
                else:
                    print(f"QuestionDetailForm with ID {id_question_detail_form} not found")
                    raise HTTPException(status_code=404, detail=f"QuestionDetailForm with ID {id_question_detail_form} not found")
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error committing transaction: {str(e)}")
            raise HTTPException(status_code=500, detail="Error saving data")
    async def generate_unique_filename(original_filename: str) -> str:

        ext = os.path.splitext(original_filename)[1]
    
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S%f')

        random_numbers = random.randint(1000, 9999)
        
        # Combinar la fecha y hora actual con el nombre original y la extensión
        new_filename = f"{current_datetime}_{random_numbers}.pdf"
        
        return new_filename
    