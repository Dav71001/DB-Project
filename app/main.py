from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from . import crud, schemas, database
from .models import apartment_models as models

app = FastAPI(title="Pro Utility API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ПУНКТ 7: Пагинация + ПУНКТ 5: Сортировка
@app.get("/apartments/", tags=["Advanced SQL"])
def read_apartments(skip: int = 0, limit: int = 10, sort_by: str = "id", db: Session = Depends(get_db)):
    return db.query(models.Apartment).order_by(getattr(models.Apartment, sort_by)).offset(skip).limit(limit).all()

# ПУНКТ 5: JOIN
@app.get("/payments/detailed/", tags=["Advanced SQL"])
def get_payments_detailed(db: Session = Depends(get_db)):
    results = db.query(models.Payment.amount, models.Apartment.owner, models.Service.name)\
        .join(models.Apartment).join(models.Service).all()
    return [{"amount": r[0], "owner": r[1], "service": r[2]} for r in results]

# ПУНКТ 5: GROUP BY
@app.get("/stats/services/", tags=["Advanced SQL"])
def get_service_stats(db: Session = Depends(get_db)):
    results = db.query(models.Service.name, func.sum(models.Payment.amount).label("total"))\
        .join(models.Payment).group_by(models.Service.name).all()
    return [{"service": r[0], "total_amount": r[1]} for r in results]

# ПУНКТ 5: UPDATE с нетривиальным условием
@app.put("/payments/increase/{street}", tags=["Advanced SQL"])
def increase_bills(street: str, db: Session = Depends(get_db)):
    subquery = db.query(models.Apartment.id).filter(models.Apartment.street == street).subquery()
    db.query(models.Payment).filter(models.Payment.apartment_id.in_(subquery))\
        .update({models.Payment.amount: models.Payment.amount * 1.1}, synchronize_session=False)
    db.commit()
    return {"status": "success", "message": f"Bills on {street} increased by 10%"}

# ПУНКТ 6: JSON + Regex поиск
@app.get("/services/search-json/", tags=["JSON & Fulltext"])
def search_json(pattern: str, db: Session = Depends(get_db)):
    return db.query(models.Service).filter(
        models.Service.extra_data.cast(database.String).op("~")(pattern)
    ).all()

# Стандартные методы для CRUD и Seed
@app.post("/apartments/", response_model=schemas.Apartment, tags=["Base CRUD"])
def create_apt(apt: schemas.ApartmentCreate, db: Session = Depends(get_db)):
    return crud.create_apartment(db, apt)

@app.post("/payments/", response_model=schemas.Payment, tags=["Base CRUD"])
def create_pay(pay: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db, pay)

@app.get("/services/", response_model=List[schemas.Service], tags=["Base CRUD"])
def get_services(db: Session = Depends(get_db)):
    return crud.get_services(db)
