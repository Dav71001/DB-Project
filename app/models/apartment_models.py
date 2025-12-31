from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Apartment(Base):
    __tablename__ = "apartments"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    house_number = Column(String)
    apartment_number = Column(String)
    owner = Column(String)
    rating = Column(Integer, default=5) 
    
    payments = relationship("Payment", back_populates="apartment")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    extra_data = Column(JSON, nullable=True) 

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2))
    payment_date = Column(DateTime)
    apartment_id = Column(Integer, ForeignKey("apartments.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    
    apartment = relationship("Apartment", back_populates="payments")