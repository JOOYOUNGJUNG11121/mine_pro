from fastapi import APIRouter, Depends, HTTPException, Query
from app.db import SessionLocal
from app.models import Customer
from app.schemas import CustomerCreate, CustomerOut
from typing import List

router = APIRouter()

@router.post('', response_model=CustomerOut, status_code=201)
def create_customer(payload: CustomerCreate):
    db = SessionLocal()
    c = Customer(name=payload.name, company=payload.company, contact_email=payload.contact_email)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get('', response_model=List[CustomerOut])
def list_customers(q: str = Query(None)):
    db = SessionLocal()
    qs = db.query(Customer)
    if q:
        qs = qs.filter(Customer.name.contains(q))
    return qs.all()

