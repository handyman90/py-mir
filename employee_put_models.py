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
    branch_id = Column(String(30), nullable=True)  # BranchID
    currency_id = Column(String(10), nullable=True)  # CurrencyID
    department_id = Column(String(30), nullable=True)  # DepartmentID
    employee_class_id = Column(String(10), nullable=True)  # EmployeeClassID
    payment_method = Column(String(10), nullable=True)  # PaymentMethod
    status = Column(String(5), nullable=True)  # Status (assuming a string for true/false)

# Pydantic model for the API request
class ValueField(BaseModel):
    value: Optional[str]  # Make value optional

class EmployeePutModel(BaseModel):
    BranchID: ValueField  # Maps to branch_id
    CurrencyID: ValueField  # Maps to currency_id
    DateOfBirth: ValueField  # Maps to tkhLahir
    DepartmentID: ValueField  # Maps to department_id
    EmployeeClassID: ValueField  # Maps to employee_class_id
    EmployeeID: ValueField  # Maps to Nokt
    Name: ValueField  # Maps to Nama
    PaymentMethod: ValueField  # Maps to payment_method
    Status: ValueField  # Maps to status
