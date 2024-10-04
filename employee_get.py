# employee_get.py

from fastapi import FastAPI, HTTPException, Header
import requests
import json
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# Token URL and payload for authentication
token_url = "http://202.75.55.71/2023R1Preprod/identity/connect/token"

# Function to authenticate and get a session token
def get_auth_token() -> str:
    payload = {
        "grant_type": "password",
        "client_id": "03407458-3136-511B-24FB-68D470104D22@MIROS 090624",
        "client_secret": "3gVM0RbnqDwXYfO1aekAyw",
        "scope": "api",
        "username": "apiuser",
        "password": "apiuser"
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

# Define the data models for the expected response structure
class CustomField(BaseModel):
    type: str
    value: Optional[str]

class Address(BaseModel):
    id: str
    rowNumber: int
    note: Optional[str]
    AddressLine1: Dict
    AddressLine2: Dict
    City: Dict
    Country: Dict
    PostalCode: Dict
    State: Dict
    custom: Dict

class EmploymentHistory(BaseModel):
    id: str
    rowNumber: int
    note: Optional[str]
    Active: Dict
    EndDate: Dict
    LineNbr: Dict
    PositionID: Dict
    RehireEligible: Dict
    StartDate: Dict
    StartReason: Dict
    Terminated: Dict
    TerminationReason: Dict
    custom: Dict

class CurrentEmployee(BaseModel):
    AcctReferenceNbr: CustomField
    UsrPlacementID: CustomField
    CalendarID: CustomField
    HoursValidation: CustomField
    SalesPersonID: CustomField
    UserID: CustomField
    AllowOverrideCury: CustomField
    CuryRateTypeID: CustomField
    AllowOverrideRate: CustomField
    LabourItemID: CustomField
    UnionID: CustomField
    RouteEmails: CustomField
    TimeCardRequired: CustomField
    NoteID: CustomField
    PrepaymentAcctID: CustomField
    PrepaymentSubID: CustomField
    ExpenseAcctID: CustomField
    ExpenseSubID: CustomField
    SalesAcctID: CustomField
    SalesSubID: CustomField
    TermsID: CustomField

class EmployeeData(BaseModel):
    id: str
    rowNumber: int
    note: Optional[str]
    BranchID: Dict
    Contact: Dict  # Adjust this based on the exact structure of Contact
    CurrencyID: Dict
    DateOfBirth: Dict
    DepartmentID: Dict
    EmployeeClassID: Dict
    EmployeeCost: List[Dict]
    EmployeeID: Dict
    EmploymentHistory: List[EmploymentHistory]
    Name: Dict
    PaymentMethod: Dict
    ReportsToID: Dict
    Status: Dict
    custom: CurrentEmployee

# Endpoint to test the token
@app.get("/test-token")
def test_token():
    try:
        token = get_auth_token()
        return {"status": "success", "token": token}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# Endpoint to retrieve employee information
@app.get("/organization/employee", response_model=EmployeeData)
def get_employee(employee_id: str, authorization: str = Header(None)):
    if authorization is None:
        authorization = get_auth_token()

    # External API URL to fetch employee information
    url = f"http://202.75.55.71/2023R1Preprod/entity/GRP9Default/1/Employee?$filter=EmployeeID eq '{employee_id}'"
    headers = {"Authorization": f"Bearer {authorization}"}

    # Fetch employee data from the external API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        employee_data = response.json()
        return EmployeeData(**employee_data)  # Return the employee data as a response
    elif response.status_code == 400:
        raise HTTPException(status_code=400, detail="Bad Request")
    elif response.status_code == 500:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        raise HTTPException(status_code=response.status_code, detail="An error occurred")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
