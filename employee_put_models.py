from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

# Use the Base defined in models.py
from models import Base

# SQLAlchemy model for the peribadi_GRP table
class Employee(Base):
    __tablename__ = 'peribadi_GRP'  # This is your table name

    Nokt = Column(String(15), primary_key=True, index=True)  # Employee ID as the primary key
    Nama = Column(String(100), nullable=True)  # Full name
    tkhLahir = Column(DateTime, nullable=True)  # Date of Birth

# Pydantic model for the API request
class ValueField(BaseModel):
    value: Optional[str]  # Make value optional

class EmployeePutModel(BaseModel):
    Nokt: ValueField
    Nama: ValueField
    tkhLahir: ValueField
