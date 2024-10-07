from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

# Define the base for SQLAlchemy models
Base = declarative_base()

# SQLAlchemy model for the peribadi_GRP table
class Employee(Base):
    __tablename__ = 'peribadi_GRP'  # This is your table name

    Nokt = Column(String(15), nullable=True)  # Assuming this is your primary key or a unique field
    Nama = Column(String(100), nullable=True)  # Full name
    Nokplama = Column(String(15), nullable=True)  # Old ID
    Nokpbaru = Column(String(15), nullable=True)  # New ID
    tkhLahir = Column(DateTime, nullable=True)  # Date of Birth

# Pydantic model for the API request
class ValueField(BaseModel):
    value: Optional[str]

class EmployeePutModel(BaseModel):
    Nokt: ValueField
    Nama: ValueField
    Nokplama: ValueField
    Nokpbaru: ValueField
    tkhLahir: ValueField
    # Add more fields according to your API needs
