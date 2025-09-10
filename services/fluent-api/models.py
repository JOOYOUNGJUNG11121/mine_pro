from sqlalchemy import Column, Integer, BigInteger, String, DateTime, JSON, Enum, Text, func
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    role = Column(Enum('user','admin','service'), default='user')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Model(Base):
    __tablename__ = "models"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    version = Column(String(50), nullable=False)
    endpoint_url = Column(String(512))
    metadata = Column(JSON)
    status = Column(Enum('staging','deployed','deprecated'), default='staging')
    created_at = Column(DateTime, server_default=func.now())

class RequestLog(Base):
    __tablename__ = "requests"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    model_id = Column(BigInteger)
    request_payload = Column(JSON)
    request_type = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class ResponseLog(Base):
    __tablename__ = "responses"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    request_id = Column(BigInteger)
    model_id = Column(BigInteger)
    response_payload = Column(JSON)
    latency_ms = Column(Integer)
    status_code = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
