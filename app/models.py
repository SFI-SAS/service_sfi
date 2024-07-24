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

class InputDetail(Base):
    __tablename__ = 'inputs_detail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_label = Column(String(255))
    type = Column(String(120))
    status =  Column(Enum(Status))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())

class Form(Base):
    __tablename__ = 'forms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_form = Column(String(255))
    desc_form = Column(String(255))
    status = Column(Enum(Status))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255))
    telephone = Column(String(20))
    rol = Column(Enum(RolUser))
    password = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())
    
class ResponseUser(Base):
    __tablename__ = 'response_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_input_detail_fom = Column(Integer, ForeignKey('input_detail_form.id'))
    form = Column(Integer, ForeignKey('forms.id'))
    id_user = Column(Integer, ForeignKey('users.id'))
    response = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())


class InputDetailForm(Base):
    __tablename__ = 'input_detail_form'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_form = Column(Integer, ForeignKey('forms.id'))
    id_input_detail = Column(Integer, ForeignKey('inputs_detail.id'))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())