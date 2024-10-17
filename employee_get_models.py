from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ValueField(BaseModel):
    value: Optional[str]

class Address(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: Optional[ValueField]
    AddressLine2: Optional[ValueField]
    City: Optional[str]
    Country: Optional[ValueField]
    PostalCode: Optional[str]
    State: Optional[str]

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    DisplayName: Optional[ValueField]
    Email: Optional[ValueField]
    Fax: Optional[str]
    FirstName: Optional[str]
    LastName: Optional[ValueField]
    MiddleName: Optional[str]
    Phone1: Optional[str]
    Phone1Type: Optional[ValueField]
    Phone2: Optional[str]
    Phone2Type: Optional[ValueField]
    Title: Optional[ValueField]
    Address: Optional[Address]

class EmploymentHistory(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: Optional[ValueField]
    EndDate: Optional[str]
    LineNbr: Optional[ValueField]
    PositionID: Optional[ValueField]
    RehireEligible: Optional[ValueField]
    StartDate: Optional[str]
    StartReason: Optional[ValueField]
    Terminated: Optional[ValueField]
    TerminationReason: Optional[str]

class PaymentInstruction(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    BAccountID: Optional[ValueField]
    Description: Optional[ValueField]
    InstructionID: Optional[ValueField]
    LocationID: Optional[ValueField]
    PaymentMethod: Optional[ValueField]
    Value: Optional[ValueField]

class EmployeeResponse(BaseModel):
    id: str
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    BranchID: Optional[ValueField]
    Calendar: Optional[ValueField]
    CashAccount: Optional[ValueField]
    Contact: Optional[Contact]
    CurrencyID: Optional[ValueField]
    DateOfBirth: Optional[ValueField]
    DepartmentID: Optional[ValueField]
    EmployeeClassID: Optional[ValueField]
    EmployeeID: Optional[ValueField]
    EmploymentHistory: List[EmploymentHistory]
    ExpenseAccount: Optional[ValueField]
    ExpenseSubaccount: Optional[ValueField]
    IdentityNumber: Optional[ValueField]
    IdentityType: Optional[ValueField]
    LastModifiedDateTime: Optional[str] = None
    Name: Optional[ValueField]
    PaymentInstruction: List[PaymentInstruction]
    PaymentMethod: Optional[ValueField]
    ReportsToID: Optional[str] = None
    SalesAccount: Optional[ValueField]
    SalesSubaccount: Optional[ValueField]
    Status: Optional[ValueField]
    Custom: Optional[Dict[str, Any]] = None
    Links: Optional[Dict[str, Any]] = None
