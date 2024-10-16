from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ValueField(BaseModel):
    value: Optional[str]  # Making it optional to match the response

class Address(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: ValueField
    AddressLine2: ValueField
    City: Optional[Dict[str, Any]]
    Country: ValueField
    PostalCode: Optional[Dict[str, Any]]
    State: Optional[Dict[str, Any]]
    custom: Optional[Dict[str, Any]]
    files: Optional[List]

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Address: Address
    DisplayName: ValueField
    Email: ValueField
    Fax: Optional[Dict[str, Any]]
    FirstName: Optional[Dict[str, Any]]
    LastName: ValueField
    MiddleName: Optional[Dict[str, Any]]
    Phone1: Optional[Dict[str, Any]]
    Phone1Type: ValueField
    Phone2: Optional[Dict[str, Any]]
    Phone2Type: ValueField
    Title: ValueField
    custom: Optional[Dict[str, Any]]
    files: Optional[List]

class EmploymentHistory(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: ValueField
    EndDate: Optional[Dict[str, Any]]
    LineNbr: ValueField
    PositionID: ValueField
    RehireEligible: ValueField
    StartDate: ValueField
    StartReason: ValueField
    Terminated: ValueField
    TerminationReason: Optional[Dict[str, Any]]
    custom: Optional[Dict[str, Any]]
    files: Optional[List]

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
    custom: Optional[Dict[str, Any]]
    files: Optional[List]

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
    ReportsToID: Optional[Dict[str, Any]] = None
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict[str, Any]] = None
    links: Optional[Dict[str, Any]] = None
