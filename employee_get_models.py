from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class ValueField(BaseModel):
    value: Optional[Union[str, int, bool]]  # Accept string, integer, or boolean

class Address(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: Optional[ValueField]
    AddressLine2: Optional[ValueField]
    City: Optional[Dict]
    Country: Optional[ValueField]
    PostalCode: Optional[Dict]
    State: Optional[Dict]
    custom: Optional[Dict]
    files: Optional[List[Dict]]

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Address: Optional[Address]
    DisplayName: Optional[ValueField]
    Email: Optional[ValueField]
    Fax: Optional[Dict]
    FirstName: Optional[Dict]
    LastName: Optional[ValueField]
    MiddleName: Optional[Dict]
    Phone1: Optional[Dict]
    Phone1Type: Optional[ValueField]
    Phone2: Optional[Dict]
    Phone2Type: Optional[ValueField]
    Title: Optional[ValueField]
    WebSite: Optional[Dict]
    custom: Optional[Dict]
    files: Optional[List[Dict]]

class EmploymentHistory(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: Optional[ValueField]  # Now accepts bool as well
    EndDate: Optional[Dict]
    LineNbr: Optional[ValueField]  # Now accepts int as well
    PositionID: Optional[ValueField]
    RehireEligible: Optional[ValueField]  # Now accepts bool as well
    StartDate: Optional[ValueField]
    StartReason: Optional[ValueField]
    Terminated: Optional[ValueField]  # Now accepts bool as well
    TerminationReason: Optional[Dict]
    custom: Optional[Dict]
    _links: Optional[Dict]
    files: Optional[List[Dict]]

class PaymentInstruction(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    BAccountID: Optional[ValueField]  # Now accepts int as well
    Description: Optional[ValueField]
    InstructionID: Optional[ValueField]
    LocationID: Optional[ValueField]  # Now accepts int as well
    PaymentMethod: Optional[ValueField]
    Value: Optional[ValueField]
    custom: Optional[Dict]
    files: Optional[List[Dict]]

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
    ReportsToID: Optional[Dict]
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict]
    _links: Optional[Dict]
    files: Optional[List[Dict]]
