
from fastapi import HTTPException, Depends
from starlette import status
from typing import Annotated
from app.models import Forms

class forms():       
    def create_new_form(db, data_form):
        new_form = Forms(
                name_form=data_form.name_form,
                desc_form=data_form.desc_form,
                status= 'inactive'
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

        
        db.commit()
        return {"message": "Form updated successfully"}
    
    def delete_form(db, data_form):
        form = db.query(Forms).filter(Forms.id == data_form.id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        
        db.delete(form)
        db.commit()
        return {"message": "Form deleted successfully"}