from pydantic import BaseModel
from typing import Optional, List, Dict

class ValueField(BaseModel):
    value: Optional[str]  # Make value optional

class Address(BaseModel):
    id: Optional[str]  # Made optional
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    AddressLine1: ValueField = None
    AddressLine2: ValueField = None
    City: Optional[Dict] = None
    Country: ValueField = None
    PostalCode: Optional[Dict] = None
    State: Optional[Dict] = None
    custom: Optional[Dict] = None
    files: Optional[List] = None

class Contact(BaseModel):
    id: Optional[str]  # Made optional
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    Address: Address = None
    DisplayName: ValueField = None
    Email: ValueField = None
    Fax: Optional[Dict] = None
    FirstName: Optional[Dict] = None
    LastName: ValueField = None
    MiddleName: Optional[Dict] = None
    Phone1: Optional[Dict] = None
    Phone1Type: ValueField = None
    Phone2: Optional[Dict] = None
    Phone2Type: ValueField = None
    Title: ValueField = None
    WebSite: Optional[Dict] = None
    custom: Optional[Dict] = None
    files: Optional[List] = None

class EmploymentHistory(BaseModel):
    id: Optional[str]  # Made optional
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    Active: ValueField = None
    EndDate: Optional[Dict] = None
    LineNbr: ValueField = None
    PositionID: ValueField = None
    RehireEligible: ValueField = None
    StartDate: ValueField = None
    StartReason: ValueField = None
    Terminated: ValueField = None
    TerminationReason: Optional[Dict] = None
    custom: Optional[Dict] = None
    _links: Optional[Dict] = None
    files: Optional[List] = None

class PaymentInstruction(BaseModel):
    id: Optional[str]  # Made optional
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    BAccountID: ValueField = None
    Description: ValueField = None
    InstructionID: ValueField = None
    LocationID: ValueField = None
    PaymentMethod: ValueField = None
    Value: ValueField = None
    custom: Optional[Dict] = None
    files: Optional[List] = None

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
    ReportsToID: Optional[Dict] = None
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict] = None
    links: Optional[Dict] = None
