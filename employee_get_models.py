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

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Activities: Optional[List[Dict]] = None  # Set to Optional
    Attributes: Optional[List[Dict]] = None  # Set to Optional
    Campaigns: Optional[List[Dict]] = None  # Set to Optional
    Cases: Optional[List[Dict]] = None  # Set to Optional
    Duplicates: Optional[List[Dict]] = None  # Set to Optional
    MarketingLists: Optional[List[Dict]] = None  # Set to Optional
    Notifications: Optional[List[Dict]] = None  # Set to Optional
    Opportunities: Optional[List[Dict]] = None  # Set to Optional
    Phone1: Optional[Dict] = None
    Phone1Type: Optional[Dict] = None
    Phone2: Optional[Dict] = None
    Phone2Type: Optional[Dict] = None
    Title: Optional[Dict] = None
    UserInfo: Optional[Dict] = None
    WebSite: Optional[Dict] = None
    custom: Optional[Dict] = None

class CurrentEmployee(BaseModel):
    AcctReferenceNbr: Optional[CustomField]
    UsrPlacementID: Optional[CustomField]
    CalendarID: Optional[CustomField]
    HoursValidation: Optional[CustomField]
    SalesPersonID: Optional[CustomField]
    UserID: Optional[CustomField]
    AllowOverrideCury: Optional[CustomField]
    CuryRateTypeID: Optional[CustomField]
    AllowOverrideRate: Optional[CustomField]
    LabourItemID: Optional[CustomField]
    UnionID: Optional[CustomField]
    RouteEmails: Optional[CustomField]
    TimeCardRequired: Optional[CustomField]
    NoteID: Optional[CustomField]
    PrepaymentAcctID: Optional[CustomField]
    PrepaymentSubID: Optional[CustomField]
    ExpenseAcctID: Optional[CustomField]
    ExpenseSubID: Optional[CustomField]
    SalesAcctID: Optional[CustomField]
    SalesSubID: Optional[CustomField]
    TermsID: Optional[CustomField]

class EmployeeResponse(BaseModel):
    id: str
    rowNumber: Optional[int]
    note: Optional[str]
    BranchID: Optional[Dict]
    Contact: Optional[Contact]
    CurrencyID: Optional[Dict]
    DateOfBirth: Optional[Dict]
    DepartmentID: Optional[Dict]
    EmployeeClassID: Optional[Dict]
    EmployeeCost: Optional[List[Dict]]  # Assuming this is optional
    EmployeeID: Optional[Dict]
    EmploymentHistory: Optional[List[EmploymentHistory]]
    Name: Optional[Dict]
    PaymentMethod: Optional[Dict]
    ReportsToID: Optional[Dict]
    Status: Optional[Dict]
    custom: Optional[Dict]
