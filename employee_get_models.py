from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# SQLAlchemy Base model
Base = declarative_base()

# SQLAlchemy model for the Employee table
class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    branch_id = Column(String, nullable=True)  # BranchID
    currency_id = Column(String, nullable=True)  # CurrencyID
    date_of_birth = Column(DateTime, nullable=True)  # DateOfBirth
    department_id = Column(String, nullable=True)  # DepartmentID
    employee_class_id = Column(String, nullable=True)  # EmployeeClassID
    name = Column(String, nullable=True)  # Name
    payment_method = Column(String, nullable=True)  # PaymentMethod
    status = Column(String, nullable=True)  # Status
    custom_fields = Column(JSON, nullable=True)  # Store custom fields as JSON

# Pydantic models for response structure
class CustomField(BaseModel):
    type: Optional[str]
    value: Optional[str]

class Address(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: Optional[Dict]
    AddressLine2: Optional[Dict]
    City: Optional[Dict]
    Country: Optional[Dict]
    PostalCode: Optional[Dict]
    State: Optional[Dict]
    custom: Optional[Dict]

class EmploymentHistory(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: Optional[Dict]
    EndDate: Optional[Dict]
    LineNbr: Optional[Dict]
    PositionID: Optional[Dict]
    RehireEligible: Optional[Dict]
    StartDate: Optional[Dict]
    StartReason: Optional[Dict]
    Terminated: Optional[Dict]
    TerminationReason: Optional[Dict]
    custom: Optional[Dict]

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Activities: Optional[List[Dict]]
    Address: Optional[Address]
    Attributes: Optional[List[Dict]]
    Campaigns: Optional[List[Dict]]
    Cases: Optional[List[Dict]]
    DisplayName: Optional[Dict]
    Duplicates: Optional[List[Dict]]
    Email: Optional[Dict]
    Fax: Optional[Dict]
    FirstName: Optional[Dict]
    LastName: Optional[Dict]
    MarketingLists: Optional[List[Dict]]
    MiddleName: Optional[Dict]
    Notifications: Optional[List[Dict]]
    Opportunities: Optional[List[Dict]]
    Phone1: Optional[Dict]
    Phone1Type: Optional[Dict]
    Phone2: Optional[Dict]
    Phone2Type: Optional[Dict]
    Relations: Optional[List[Dict]]
    Title: Optional[Dict]
    UserInfo: Optional[Dict]
    WebSite: Optional[Dict]
    custom: Optional[Dict]

class CurrentEmployee(BaseModel):
    AcctReferenceNbr: Optional[CustomField]
    UsrPlacementID: Optional[CustomField]
    CalendarID: Optional[CustomField]
    HoursValidation: Optional[CustomField]
    SalesPersonID: Optional[CustomField]
    UserID: Optional[CustomField]
    AllowOverrideCury: Optional[CustomField]
    CuryRateTypeID: Optional[CustomField]
    AllowOverrideRate: Optional[CustomField]
    LabourItemID: Optional[CustomField]
    UnionID: Optional[CustomField]
    RouteEmails: Optional[CustomField]
    TimeCardRequired: Optional[CustomField]
    NoteID: Optional[CustomField]
    PrepaymentAcctID: Optional[CustomField]
    PrepaymentSubID: Optional[CustomField]
    ExpenseAcctID: Optional[CustomField]
    ExpenseSubID: Optional[CustomField]
    SalesAcctID: Optional[CustomField]
    SalesSubID: Optional[CustomField]
    TermsID: Optional[CustomField]

class DefLocation(BaseModel):
    VAPAccountID: Optional[CustomField]
    VAPSubID: Optional[CustomField]
    NoteID: Optional[CustomField]
    VTaxZoneID: Optional[CustomField]
    VPaymentMethodID: Optional[CustomField]
    VCashAccountID: Optional[CustomField]

class EmployeeResponse(BaseModel):
    id: str
    rowNumber: Optional[int]
    note: Optional[str]
    BranchID: Optional[Dict]
    Contact: Optional[Contact]
    CurrencyID: Optional[Dict]
    DateOfBirth: Optional[Dict]
    DepartmentID: Optional[Dict]
    EmployeeClassID: Optional[Dict]
    EmployeeCost: Optional[List[Dict]]
    EmployeeID: Optional[Dict]
    EmploymentHistory: Optional[List[EmploymentHistory]]
    Name: Optional[Dict]
    PaymentMethod: Optional[Dict]
    ReportsToID: Optional[Dict]
    Status: Optional[Dict]
    custom: Optional[Dict]
    DefLocation: Optional[DefLocation]
