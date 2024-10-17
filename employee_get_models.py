from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ValueField(BaseModel):
    value: Optional[str]  # Make value optional

class Link(BaseModel):
    self: Optional[str]
    files_put: Optional[str]

class Contact(BaseModel):
    id: str
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    DisplayName: ValueField
    Email: ValueField
    Fax: ValueField
    FirstName: ValueField
    LastName: ValueField
    MiddleName: ValueField
    Phone1: ValueField
    Phone1Type: ValueField
    Phone2: ValueField
    Phone2Type: ValueField
    Title: ValueField

class Address(BaseModel):
    id: str
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    AddressLine1: ValueField
    AddressLine2: ValueField
    City: ValueField
    Country: ValueField
    PostalCode: ValueField
    State: ValueField

class EmploymentHistory(BaseModel):
    id: str
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    Active: ValueField
    EndDate: Optional[Dict[str, Any]] = None
    LineNbr: ValueField
    PositionID: ValueField
    RehireEligible: ValueField
    StartDate: ValueField
    StartReason: ValueField
    Terminated: ValueField
    TerminationReason: Optional[Dict[str, Any]] = None

class PaymentInstruction(BaseModel):
    id: str
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    BAccountID: ValueField
    Description: ValueField
    InstructionID: ValueField
    LocationID: ValueField
    PaymentMethod: ValueField
    Value: ValueField

class EmployeeResponse(BaseModel):
    id: str
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    BranchID: ValueField
    Calendar: ValueField
    CashAccount: ValueField
    Contact: Contact
    CurrencyID: ValueField
    DateOfBirth: ValueField
    DepartmentID: ValueField
    EmployeeClassID: ValueField
    EmployeeID: ValueField
    EmploymentHistory: List[EmploymentHistory]
    ExpenseAccount: ValueField
    ExpenseSubaccount: ValueField
    IdentityNumber: ValueField
    IdentityType: ValueField
    LastModifiedDateTime: ValueField
    Name: ValueField
    PaymentInstruction: List[PaymentInstruction]
    PaymentMethod: ValueField
    ReportsToID: Optional[str] = None
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict[str, Any]] = None
    links: Link
