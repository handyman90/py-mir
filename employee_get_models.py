from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Pydantic models for response structure

class ValueField(BaseModel):
    value: Optional[str]  # Make value optional

class Address(BaseModel):
    id: Optional[str]  # Unique identifier
    rowNumber: Optional[int]  # Row number
    note: Optional[str]  # Note field
    AddressLine1: ValueField
    AddressLine2: ValueField
    City: Optional[Dict[str, Any]]  # Additional fields as required
    Country: ValueField
    PostalCode: Optional[Dict[str, Any]]
    State: Optional[Dict[str, Any]]
    custom: Optional[Dict[str, Any]]
    files: Optional[List[Dict[str, Any]]]  # Assuming files can be a list of dictionaries

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
    files: Optional[List[Dict[str, Any]]]

class PaymentInstruction(BaseModel):
    id: str
    rowNumber: Optional[int]
    note: Optional[str]
    BAccountID: ValueField
    Description: ValueField
    InstructionID: ValueField
    LocationID: ValueField
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
