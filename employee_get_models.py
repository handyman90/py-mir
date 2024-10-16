from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Pydantic models for response structure

class ValueField(BaseModel):
    value: Optional[str]  # Make value optional

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
    files: Optional[List[Dict[str, Any]]]

class Contact(BaseModel):
    id: str
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
    WebSite: Optional[Dict[str, Any]]
    custom: Optional[Dict[str, Any]]
    files: Optional[List[Dict[str, Any]]]

class EmploymentHistory(BaseModel):
    id: str
    rowNumber: Optional[int]
    note: Optional[str]
    Active: ValueField  # Change to ValueField to hold 'true'/'false' as strings
    EndDate: Optional[Dict[str, Any]]
    LineNbr: ValueField  # Change to ValueField to hold the line number as string
    PositionID: ValueField
    RehireEligible: ValueField  # Change to ValueField to hold 'true'/'false' as strings
    StartDate: ValueField
    StartReason: ValueField
    Terminated: ValueField  # Change to ValueField to hold 'true'/'false' as strings
    TerminationReason: Optional[Dict[str, Any]]
    custom: Optional[Dict[str, Any]]
    files: Optional[List[Dict[str, Any]]]

class PaymentInstruction(BaseModel):
    id: str
    rowNumber: Optional[int]
    note: Optional[str]
    BAccountID: ValueField  # Change to ValueField to hold as string
    Description: ValueField
    InstructionID: ValueField
    LocationID: ValueField  # Change to ValueField to hold as string
    PaymentMethod: ValueField
    Value: ValueField
    custom: Optional[Dict[str, Any]]
    files: Optional[List[Dict[str, Any]]]

class EmployeeResponse(BaseModel):
    id: str
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
    LastModifiedDateTime: ValueField
    Name: ValueField
    PaymentInstruction: List[PaymentInstruction]
    PaymentMethod: ValueField
    ReportsToID: Optional[Dict[str, Any]]
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict[str, Any]]
    links: Optional[Dict[str, Any]]  # To hold links in the response
