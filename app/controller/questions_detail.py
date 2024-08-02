
from fastapi import HTTPException
from starlette import status
from app.models import QuestionDetailForm, QuestionsDetail


class questions_detail():       
    def new_questions_detail(db, data_question):
        try:
            questions_details = [
                QuestionsDetail(
                    name_label=data.name_label,
                    type=data.type,
                    status=data.status
                ) for data in data_question.data
            ]
            db.add_all(questions_details)
            db.commit()

            for question_detail in questions_details:
                db.refresh(question_detail)

            question_detail_forms = [
                QuestionDetailForm(
                    id_forms=data_question.id_form,
                    id_quiestions_detail=question_detail.id,
                    position=data.position
                ) for data, question_detail in zip(data_question.data, questions_details)
            ]
            db.add_all(question_detail_forms)
            db.commit()

            return data_question
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


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

        
        positios_form = db.query(QuestionDetailForm).filter(QuestionDetailForm.id_quiestions_detail == result_question.id).first()

        if data_question.position:
            positios_form.position = data_question.position
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
