from os import environ

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response
from prometheus_client.utils import INF
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from sqlalchemy.orm import Session
from starlette import status

from .schemas import users as schemas
from .models import users as models
from .models.database import SessionLocal

app = FastAPI()
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"HOSTNAME": environ.get('HOSTNAME')}


@app.get("/health")
def read_root():
    return {"status": "OK"}


@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, first_name=user.first_name, last_name=user.last_name,
                          email=user.email, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/user/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email
    db_user.phone = user.phone
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/user/{user_id}", status_code=204)
def update_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
