from sqlalchemy import Column, Integer, BigInteger, String, DateTime, JSON, Enum, func, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255))
    contact_email = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    events = relationship('Event', back_populates='customer')

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('admin','analyst'), default='analyst')
    created_at = Column(DateTime, server_default=func.now())

class Event(Base):
    __tablename__ = "events"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(BigInteger, ForeignKey('customers.id'), nullable=False)
    event_type = Column(String(100))
    severity = Column(Enum('low','medium','high','critical'), default='low')
    event_time = Column(DateTime, nullable=False)
    raw_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    customer = relationship('Customer', back_populates='events')
    alerts = relationship('Alert', back_populates='event')

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey('events.id'), nullable=False)
    status = Column(Enum('triggered','ack','resolved'), default='triggered')
    notified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    event = relationship('Event', back_populates='alerts')

