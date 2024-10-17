from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Value Field Pydantic model for consistent structure
class ValueField(BaseModel):
    value: Optional[str]  # All fields are optional

# Pydantic models for the expected response structure
class ContactAddress(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: Optional[ValueField]
    AddressLine2: Optional[ValueField]
    City: Optional[Dict[str, Any]]
    Country: Optional[ValueField]
    PostalCode: Optional[Dict[str, Any]]
    State: Optional[Dict[str, Any]]

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Address: Optional[ContactAddress]
    DisplayName: Optional[ValueField]
    Email: Optional[ValueField]
    Fax: Optional[ValueField]
    FirstName: Optional[ValueField]
    LastName: Optional[ValueField]
    MiddleName: Optional[ValueField]
    Phone1: Optional[ValueField]
    Phone1Type: Optional[ValueField]
    Phone2: Optional[ValueField]
    Phone2Type: Optional[ValueField]
    Title: Optional[ValueField]

class EmploymentHistory(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: Optional[ValueField]
    EndDate: Optional[Dict[str, Any]]
    LineNbr: Optional[ValueField]
    PositionID: Optional[ValueField]
    RehireEligible: Optional[ValueField]
    StartDate: Optional[ValueField]
    StartReason: Optional[ValueField]
    Terminated: Optional[ValueField]
    TerminationReason: Optional[Dict[str, Any]]

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
    rowNumber: Optional[int]
    note: Optional[str]
    BranchID: ValueField
    Calendar: ValueField
    CashAccount: ValueField
    Contact: Optional[Contact]
    CurrencyID: ValueField
    DateOfBirth: ValueField
    DepartmentID: ValueField
    EmployeeClassID: ValueField
    EmployeeID: ValueField
    EmploymentHistory: Optional[List[EmploymentHistory]]
    ExpenseAccount: ValueField
    ExpenseSubaccount: ValueField
    IdentityNumber: ValueField
    IdentityType: ValueField
    LastModifiedDateTime: ValueField
    Name: ValueField
    PaymentInstruction: Optional[List[PaymentInstruction]]
    PaymentMethod: ValueField
    ReportsToID: Optional[Dict[str, Any]]
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict[str, Any]]
    _links: Optional[Dict[str, Any]]
