from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CustomField(BaseModel):
    type: Optional[str]
    value: Optional[str]

class Address(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: Optional[Dict]
    AddressLine2: Optional[Dict]
    City: Optional[Dict]
    Country: Optional[Dict]
    PostalCode: Optional[Dict]
    State: Optional[Dict]
    custom: Optional[Dict]

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Address: Optional[Address]
    Activities: Optional[List[Dict]] = None
    Attributes: Optional[List[Dict]] = None
    Campaigns: Optional[List[Dict]] = None
    Cases: Optional[List[Dict]] = None
    Duplicates: Optional[List[Dict]] = None
    MarketingLists: Optional[List[Dict]] = None
    Notifications: Optional[List[Dict]] = None
    Opportunities: Optional[List[Dict]] = None
    Phone1: Optional[Dict] = None
    Phone1Type: Optional[Dict] = None
    Phone2: Optional[Dict] = None
    Phone2Type: Optional[Dict] = None
    Title: Optional[Dict] = None
    UserInfo: Optional[Dict] = None
    WebSite: Optional[Dict] = None
    custom: Optional[Dict] = None
    files: Optional[List[Dict]] = None

class EmploymentHistory(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: Optional[Dict]
    EndDate: Optional[Dict]
    LineNbr: Optional[Dict]
    PositionID: Optional[Dict]
    RehireEligible: Optional[Dict]
    StartDate: Optional[Dict]
    StartReason: Optional[Dict]
    Terminated: Optional[Dict]
    TerminationReason: Optional[Dict]
    custom: Optional[Dict]

class EmployeeResponse(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    BranchID: Optional[Dict]
    Calendar: Optional[Dict]
    CashAccount: Optional[Dict]
    Contact: Optional[Contact]
    CurrencyID: Optional[Dict]
    DateOfBirth: Optional[Dict]
    DepartmentID: Optional[Dict]
    EmployeeClassID: Optional[Dict]
    EmployeeID: Optional[Dict]
    Name: Optional[Dict]
    PaymentMethod: Optional[Dict]
    Status: Optional[Dict]
    EmploymentHistory: Optional[List[EmploymentHistory]]
    custom: Optional[Dict]
