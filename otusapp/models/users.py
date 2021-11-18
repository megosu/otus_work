import sqlalchemy
from sqlalchemy import Column, Integer, String

from .database import Base

metadata = sqlalchemy.MetaData()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
