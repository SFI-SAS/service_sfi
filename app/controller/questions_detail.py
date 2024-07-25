
from fastapi import HTTPException, Depends
from starlette import status
from typing import Annotated
from app.models import QuestionDetailForm, QuestionsDetail


class questions_detail():       
    def new_questions_detail(db, data_question):
        new_form = QuestionsDetail(
                name_label=data_question.name_label,
                type=data_question.type,
                status= data_question.status
            )

        db.add(new_form)
        db.commit()
        db.refresh(new_form)  

        new_question_detail_form = QuestionDetailForm(
            id_forms=data_question.id_forms,
            id_quiestions_detail=new_form.id
        )

        db.add(new_question_detail_form)
        db.commit()

        return {"message": "questions_detail created successfully"}
    
    def update_question(db, data_question):

        result_question = db.query(QuestionsDetail).filter(QuestionsDetail.id == data_question.id).first()
        if not result_question:
            raise HTTPException(status_code=404, detail="Form not found")
        
        if data_question.name_label:
            result_question.name_label = data_question.name_label
        if data_question.type:
            result_question.type = data_question.type
        if data_question.status:
            result_question.status = data_question.status
        db.commit()
        return {"message": "questions_detail updated successfully"}
    

    def delete_question(db, data_question):
        result_question = db.query(QuestionsDetail).filter(QuestionsDetail.id == data_question.id).first()
        reference_question = db.query(QuestionDetailForm).filter(QuestionDetailForm.id_quiestions_detail == data_question.id).first()

        if not result_question:
            raise HTTPException(status_code=404, detail="Form not found")
        try:
            db.delete(reference_question)
            db.commit()
            
            db.delete(result_question)
            db.commit()
            return {"message": "result_question deleted successfully"}
            
        except Exception as e:
            db.rollback()  
            raise e  #
