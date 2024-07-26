
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import join
from starlette import status
from typing import Annotated
from app.models import Forms, QuestionDetailForm, QuestionsDetail, ResponseUser
from sqlalchemy.orm import aliased



class forms():       
    def create_new_form(db, data_form):
        new_form = Forms(
                name_form=data_form.name_form,
                desc_form=data_form.desc_form,
                status= data_form.status
            )

        db.add(new_form)
        db.commit()

        return {"message": "Form created successfully"}
    
    def update_form(db, data_form):
        form = db.query(Forms).filter(Forms.id == data_form.id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        
        if data_form.name_form:
            form.name_form = data_form.name_form
        if data_form.desc_form:
            form.desc_form = data_form.desc_form
        if data_form.status:
            form.status = data_form.status
        db.commit()
        return {"message": "Form updated successfully"}
    
    def delete_form(db, data_form):
        form = db.query(Forms).filter(Forms.id == data_form.id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        
        db.delete(form)
        db.commit()
        return {"message": "Form deleted successfully"}
    


    def get_form(db, form_id, user_rol):

        question_detail_alias = aliased(QuestionsDetail)
        question_detail_form_alias = aliased(QuestionDetailForm)

        form_details = db.query(
            Forms.id,
            Forms.name_form,
            Forms.desc_form,
            Forms.status,
            question_detail_form_alias.id.label('question_detail_form_id'),
            question_detail_alias.id.label('question_detail_id'),
            question_detail_alias.name_label,
            question_detail_alias.type,
            question_detail_alias.status.label('question_detail_status'),
            question_detail_form_alias.position.label('question_detail_form_position'),
        ).join(
            question_detail_form_alias, Forms.id == question_detail_form_alias.id_forms
        ).join(
            question_detail_alias, question_detail_form_alias.id_quiestions_detail == question_detail_alias.id
        ).filter(
            Forms.id == form_id
        ).all()

        if not form_details:
            raise HTTPException(status_code=404, detail="Form not found or no related questions")

        if user_rol == 'client' and  form_details[0].status.value == 'active':
            form_data = {
                "name_form": form_details[0].name_form,
                "desc_form": form_details[0].desc_form,
                "status": form_details[0].status,
                "data": []
            }

            for detail in form_details:
                if detail.question_detail_status.value == 'active':
                    form_data["data"].append({
                        "id": detail.question_detail_id,
                        "name_label": detail.name_label,
                        "type": detail.type,
                        "status": detail.question_detail_status,
                        "position": detail.question_detail_form_position
                    })
            return form_data
        else:
            return []

    def get_all_form(db,user_rol):
        if user_rol == 'client':
            forms = db.query(Forms).filter(Forms.status == 'active').all()
            if not forms:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No forms found"
                )
            result = [
            {
                "id": form.id,
                "name_form": form.name_form,
                "desc_form": form.desc_form,
                "status": form.status
            }
            for form in forms
            ]
        
            return result
        else:
            return []