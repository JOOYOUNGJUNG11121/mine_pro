from sqlalchemy import Column, Integer, BigInteger, String, DateTime, JSON, Enum, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(255))
    role = Column(Enum('user','admin'), default='user')
    created_at = Column(DateTime, server_default=func.now())
    devices = relationship('Device', back_populates='owner')
    consumption = relationship('Consumption', back_populates='user')

class Device(Base):
    __tablename__ = "devices"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    device_name = Column(String(255))
    device_type = Column(String(100))
    metadata = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    owner = relationship('User', back_populates='devices')
    consumption = relationship('Consumption', back_populates='device')

class Consumption(Base):
    __tablename__ = "consumption"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    device_id = Column(BigInteger, ForeignKey('devices.id'), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    energy_kwh = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship('User', back_populates='consumption')
    device = relationship('Device', back_populates='consumption')

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    device_id = Column(BigInteger, ForeignKey('devices.id'), nullable=True)
    recommended_action = Column(String(1000))
    estimated_saving = Column(Float)
    generated_at = Column(DateTime, server_default=func.now())
    metadata = Column(JSON)

