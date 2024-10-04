# employee_get.py

from fastapi import FastAPI, HTTPException, Header
import requests
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# Token URL and payload for authentication
token_url = "http://202.75.55.71/2023R1Preprod/identity/connect/token"

# Function to authenticate and get a session token
def get_auth_token() -> dict:
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
        return response.json()  # Return the entire token response
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
    Contact: Dict  # The Contact field will need to match the structure returned
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

# Define a model for the token response
class TokenResponseModel(BaseModel):
    access_token: str
    token_type: str
    expires_in: int  # The expiration time in seconds
    scope: str

# Endpoint to test the token
@app.get("/test-token", response_model=TokenResponseModel)
def test_token():
    try:
        token_response = get_auth_token()  # Get the complete token response
        return {
            "access_token": token_response.get("access_token"),
            "token_type": token_response.get("token_type"),
            "expires_in": token_response.get("expires_in"),
            "scope": token_response.get("scope")
        }
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# Endpoint to retrieve employee information
@app.get("/organization/employee", response_model=EmployeeData)
def get_employee(employee_id: str, authorization: Optional[str] = Header(None)):
    try:
        # If no authorization token is provided in the header, get a new token
        if authorization is None:
            token_response = get_auth_token()  # Retrieve a new token
            authorization = token_response.get("access_token")  # Use the access_token

        # External API URL to fetch employee information
        url = "http://202.75.55.71/2023R1Preprod/entity/GRP9Default/1/Employee"

        # Prepare the payload for the GET request
        payload = {
            "$filter": f"EmployeeID eq '{employee_id}'"
        }
        
        # Include the authorization token in the headers
        headers = {
            "Authorization": f"Bearer {authorization}",  # Use the retrieved token
            'Content-Type': 'application/json'  # Setting content type
        }

        # Log the request URL and headers for debugging
        print(f"Requesting URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Payload: {payload}")

        # Fetch employee data from the external API
        response = requests.get(url, headers=headers, params=payload)  # Pass payload as query parameters

        # Log the response status code and content
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            employee_data = response.json()

            # Check if the response is a list or a single dictionary
            if isinstance(employee_data, list) and employee_data:
                # Assuming the first element is the relevant employee data
                employee_data = employee_data[0]
            elif not isinstance(employee_data, dict):
                raise HTTPException(status_code=500, detail="Unexpected response format")

            return EmployeeData(**employee_data)  # Return the employee data as a response
        
        elif response.status_code == 400:
            raise HTTPException(status_code=400, detail="Bad Request")
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized - Please check your access token")
        elif response.status_code == 403:
            raise HTTPException(status_code=403, detail="Forbidden - Access denied")
        elif response.status_code == 500:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        else:
            raise HTTPException(status_code=response.status_code, detail="An error occurred")
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Log any unexpected exceptions
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
