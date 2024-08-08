import enum
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Status(enum.Enum):
    active = 'active'
    inactive = 'inactive'

class RolUser(enum.Enum):
    user = 'user'
    admin = 'admin'
    client = 'client'

class UserType(enum.Enum):
    text = 'text'
    file = 'file'

class QuestionsDetail(Base):
    __tablename__ = 'questions_detail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_label = Column(String(255))
    type = Column(Enum(UserType))
    status =  Column(Enum(Status))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())

class Forms(Base):
    __tablename__ = 'forms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_form = Column(String(255), unique=True)
    desc_form = Column(String(255))
    status = Column(Enum(Status))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    num_document = Column(String(50), unique=True)
    full_name = Column(String(255))
    telephone = Column(String(20), unique=True)
    email = Column(String(120), unique=True)
    rol = Column(Enum(RolUser))
    password = Column(String(255))
    status = Column(Enum(Status))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())
    
class ResponseUser(Base):
    __tablename__ = 'response_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_question_detail_form = Column(Integer, ForeignKey('question_detail_form.id'))
    id_form = Column(Integer, ForeignKey('forms.id'))
    id_user = Column(Integer, ForeignKey('users.id'))
    response = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())


class QuestionDetailForm(Base):
    __tablename__ = 'question_detail_form'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_forms = Column(Integer, ForeignKey('forms.id'))
    id_quiestions_detail = Column(Integer, ForeignKey('questions_detail.id'))
    position =  Column(String(55))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())


class UsersRefsForm(Base):
    __tablename__ = 'users_refs_form'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    id_form = Column(Integer, ForeignKey('forms.id'))
    reference = Column(String(55))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())
