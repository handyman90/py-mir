from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class ValueField(BaseModel):
    value: Optional[Union[str, Dict]]

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
    Fax: Optional[Union[Dict, ValueField]]  # Updated
    FirstName: Optional[Union[Dict, ValueField]]  # Updated
    LastName: ValueField
    MiddleName: Optional[Union[Dict, ValueField]]  # Updated
    Phone1: Optional[Union[Dict, ValueField]]  # Updated
    Phone1Type: ValueField
    Phone2: Optional[Union[Dict, ValueField]]  # Updated
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
    id: str
    rowNumber: Optional[int]
    note: Optional[str]
    BranchID: ValueField
    Calendar: ValueField
    CashAccount: ValueField
    CurrencyID: ValueField
    DateOfBirth: ValueField
    DepartmentID: ValueField
    EmployeeClassID: ValueField
    EmployeeID: ValueField
    ExpenseAccount: ValueField
    ExpenseSubaccount: ValueField
    IdentityNumber: ValueField
    IdentityType: ValueField
    LastModifiedDateTime: Optional[str]
    Name: ValueField
    PaymentMethod: ValueField
    ReportsToID: Optional[Dict]
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    Custom: Optional[Dict]
    Links: Optional[Dict]
    Contact: Contact
    EmploymentHistory: List[EmploymentHistory]
    PaymentInstruction: List[PaymentInstruction]
