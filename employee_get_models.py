from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Use the Base defined in models.py
from models import Base

# SQLAlchemy model for the employees table
class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    branch_id = Column(String, nullable=True)  # BranchID
    calendar = Column(String, nullable=True)  # Calendar
    cash_account = Column(String, nullable=True)  # CashAccount
    currency_id = Column(String, nullable=True)  # CurrencyID
    date_of_birth = Column(DateTime, nullable=True)  # DateOfBirth
    department_id = Column(String, nullable=True)  # DepartmentID
    employee_class_id = Column(String, nullable=True)  # EmployeeClassID
    expense_account = Column(String, nullable=True)  # ExpenseAccount
    expense_subaccount = Column(String, nullable=True)  # ExpenseSubaccount
    identity_number = Column(String, nullable=True)  # IdentityNumber
    identity_type = Column(String, nullable=True)  # IdentityType
    last_modified_date_time = Column(DateTime, nullable=True)  # LastModifiedDateTime
    name = Column(String, nullable=True)  # Name
    payment_method = Column(String, nullable=True)  # PaymentMethod
    reports_to_id = Column(String, nullable=True)  # ReportsToID
    sales_account = Column(String, nullable=True)  # SalesAccount
    sales_subaccount = Column(String, nullable=True)  # SalesSubaccount
    status = Column(String, nullable=True)  # Status
    custom_fields = Column(JSON, nullable=True)  # Store custom fields as JSON
    links = Column(JSON, nullable=True)  # Store links as JSON

# Pydantic model for the API response
class EmployeeGetModel(BaseModel):
    employee_id: Optional[str]
    row_number: Optional[int]
    note: Optional[str]
    branch_id: Optional[str]
    calendar: Optional[str]
    cash_account: Optional[str]
    currency_id: Optional[str]
    date_of_birth: Optional[str]
    department_id: Optional[str]
    employee_class_id: Optional[str]
    expense_account: Optional[str]
    expense_subaccount: Optional[str]
    identity_number: Optional[str]
    identity_type: Optional[str]
    last_modified_date_time: Optional[str]
    name: Optional[str]
    payment_method: Optional[str]
    reports_to_id: Optional[Dict[str, Any]] = None
    sales_account: Optional[str]
    sales_subaccount: Optional[str]
    status: Optional[str]
    custom_fields: Optional[Dict[str, Any]] = None
    links: Optional[Dict[str, Any]] = None
