import datetime
import os
from fastapi import HTTPException, Depends, status as http_status
from fastapi.security import OAuth2PasswordBearer
from app.controller.mail import send_email_password
from app.models import Users
from passlib.context import CryptContext
from starlette import status
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Annotated
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class user():

    def register_new_user(db, user_register):
        hashed_password = pwd_context.hash(user_register.password)
        new_user = Users(
            num_document=user_register.num_document,
            full_name=user_register.full_name,
            telephone=user_register.telephone,
            email=user_register.email,
            rol="user",
            password=hashed_password,
            status="inactive"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    async def login_access(form_data, db):  
        user = authenticate_user(form_data.username, form_data.password, db)  

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='No se ha podido validar el usuario. Email o contraseña incorrectos.')


        token = create_access_token(user.email, user.id, timedelta(hours=24))
        
        return {'access_token': token, 'token_type': 'bearer'}

    async def valid_token_user(token: Annotated[str, Depends(oauth2_bearer)], db):  # type: ignore
        try:
          
            payload = jwt.decode(token, secret_key, algorithms=[algorithm]) # type: ignore
            email: str = payload.get('sub') # type: ignore
            user_id: int = payload.get('id') # type: ignore

            user = db.query(Users).filter(Users.email == email).first()
            
            # Verificar si el email o user_id son None
            if email is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='No se ha podido validar el usuario.'
                )

            # Buscar al usuario por email
            user = db.query(Users).filter(Users.email == email).first()

            # Verificar si el usuario fue encontrado
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )

            # Crear el diccionario del usuario
            user_dict = {
                "id": user.id,
                "num_document": user.num_document,
                "full_name": user.full_name,
                "telephone": user.telephone,
                "email": user.email,
                "rol": user.rol.value,
            }

            # Retornar la información del usuario y del token
            return {'username': email, 'id': user_id, 'user': user_dict}

        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token inválido o expirado.'
            )
        
    async def handle_reset_password_email(db, email: str):
            user = db.query(Users).filter(Users.email == email).first()
            if user:
                token_data = {"sub": user.email, "id": user.id}
                token = jwt.encode(token_data, secret_key, algorithm=algorithm)
                send_email_password(email, token)
                return {"mensaje": "Correo enviado con éxito", "token":token}
            else:
                raise HTTPException(status_code=400, detail='Usuario no encontrado') 

    async def reset_password(db, token: str, new_password: str):
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')

            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail='No se ha podido validar el usuario.')

            user = db.query(Users).filter(Users.id == user_id, Users.email == username).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail='No se ha podido validar el usuario.')

            hashed_password = bcrypt_context.hash(new_password)
            user.password = hashed_password
            db.add(user)
            db.commit()
            db.refresh(user)

            return {"mensaje": "Contraseña restablecida correctamente"}

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='No se ha podido validar el usuario')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f'No se ha podido restablecer la contraseña: {str(e)}')
        

    def activate_user_status(email,db):
        user = db.query(Users).filter(Users.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        user.status = "active" 
        db.commit()
        
        return {"mensaje": True}


    def get_active_user_by_id(db , user_id: int):
        # Buscar el usuario por ID
        user = db.query(Users).filter(Users.id == user_id).first()

        # Verificar si el usuario existe
        if not user:
            raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        # Verificar si el status es 'active'
        if user.status != 'active':
            raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="El usuario no está activo")

        # Retornar el usuario si está activo
        return user


def authenticate_user(username: str, password: str, db): # type: ignore

    user = db.query(Users).filter(Users.email == username).first()

    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def create_access_token(num_document: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': str(num_document), 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, secret_key, algorithm=algorithm)