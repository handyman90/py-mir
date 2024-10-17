from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ValueField(BaseModel):
    value: Optional[str]

class Address(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: ValueField
    AddressLine2: ValueField
    City: Optional[Dict]
    Country: ValueField
    PostalCode: Optional[Dict]
    State: Optional[Dict]
    custom: Optional[Dict]
    files: List[Dict]

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Address: Address
    DisplayName: ValueField
    Email: ValueField
    Fax: Optional[Dict]
    FirstName: Optional[Dict]
    LastName: ValueField
    MiddleName: Optional[Dict]
    Phone1: Optional[Dict]
    Phone1Type: ValueField
    Phone2: Optional[Dict]
    Phone2Type: ValueField
    Title: ValueField
    WebSite: Optional[Dict]
    custom: Optional[Dict]
    files: List[Dict]

class EmploymentHistory(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: ValueField
    EndDate: Optional[Dict]
    LineNbr: ValueField
    PositionID: ValueField
    RehireEligible: ValueField
    StartDate: ValueField
    StartReason: ValueField
    Terminated: ValueField
    TerminationReason: Optional[Dict]
    custom: Optional[Dict]
    files: List[Dict]

class PaymentInstruction(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    BAccountID: ValueField
    Description: ValueField
    InstructionID: ValueField
    LocationID: ValueField
    PaymentMethod: ValueField
    Value: ValueField
    custom: Optional[Dict]
    files: List[Dict]

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
    ReportsToID: Optional[Dict]
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict]
    _links: Optional[Dict]
    files: List[Dict]
