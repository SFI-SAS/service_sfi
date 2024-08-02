
from fastapi import HTTPException
from app.models import QuestionDetailForm, ResponseUser, UsersRefsForm


class response_user():       

    def new_response_user(db,user_id,id_form, data,reference):

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

                db_users_refs_form = UsersRefsForm(
                    id_user=user_id,
                    id_form=id_form,
                    reference=reference,
                )
                db.add(db_users_refs_form)
            else:
                raise HTTPException(status_code=404, detail=f"QuestionDetailForm with ID {text_entry.id_question_detail_form} not found")
        db.commit()
