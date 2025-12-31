from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    class Config:
        from_attributes = True

class ApartmentBase(BaseModel):
    street: str
    house_number: str
    apartment_number: str
    owner: str

class ApartmentCreate(ApartmentBase):
    pass

class Apartment(ApartmentBase):
    id: int
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    apartment_id: int
    service_id: int
    amount: Decimal
    payment_date: Optional[datetime] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    class Config:
        from_attributes = True
