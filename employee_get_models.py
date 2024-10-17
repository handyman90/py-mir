from pydantic import BaseModel
from typing import Optional, List, Dict

class ValueField(BaseModel):
    value: Optional[str]  # Optional since the value can be empty

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

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
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
    Address: Address

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

class EmployeeResponse(BaseModel):
    id: str  # Required
    rowNumber: Optional[int]
    note: Optional[str]
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
    LastModifiedDateTime: Optional[str]
    Name: ValueField
    PaymentInstruction: List[PaymentInstruction]
    PaymentMethod: ValueField
    ReportsToID: Optional[Dict]
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    Custom: Optional[Dict]
    Links: Optional[Dict]
