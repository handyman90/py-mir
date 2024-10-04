# employee_get.py

from fastapi import FastAPI, HTTPException, Header
import requests
from pydantic import BaseModel, ValidationError
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
    type: Optional[str]  # Made optional
    value: Optional[str]  # Made optional

class Address(BaseModel):
    id: Optional[str]  # Made optional
    rowNumber: Optional[int]  # Made optional
    note: Optional[str]  # Made optional
    AddressLine1: Optional[Dict]  # Made optional
    AddressLine2: Optional[Dict]  # Made optional
    City: Optional[Dict]  # Made optional
    Country: Optional[Dict]  # Made optional
    PostalCode: Optional[Dict]  # Made optional
    State: Optional[Dict]  # Made optional
    custom: Optional[Dict]  # Made optional

class EmploymentHistory(BaseModel):
    id: Optional[str]  # Made optional
    rowNumber: Optional[int]  # Made optional
    note: Optional[str]  # Made optional
    Active: Optional[Dict]  # Made optional
    EndDate: Optional[Dict]  # Made optional
    LineNbr: Optional[Dict]  # Made optional
    PositionID: Optional[Dict]  # Made optional
    RehireEligible: Optional[Dict]  # Made optional
    StartDate: Optional[Dict]  # Made optional
    StartReason: Optional[Dict]  # Made optional
    Terminated: Optional[Dict]  # Made optional
    TerminationReason: Optional[Dict]  # Made optional
    custom: Optional[Dict]  # Made optional

class CurrentEmployee(BaseModel):
    AcctReferenceNbr: Optional[CustomField]  # Made optional
    UsrPlacementID: Optional[CustomField]  # Made optional
    CalendarID: Optional[CustomField]  # Made optional
    HoursValidation: Optional[CustomField]  # Made optional
    SalesPersonID: Optional[CustomField]  # Made optional
    UserID: Optional[CustomField]  # Made optional
    AllowOverrideCury: Optional[CustomField]  # Made optional
    CuryRateTypeID: Optional[CustomField]  # Made optional
    AllowOverrideRate: Optional[CustomField]  # Made optional
    LabourItemID: Optional[CustomField]  # Made optional
    UnionID: Optional[CustomField]  # Made optional
    RouteEmails: Optional[CustomField]  # Made optional
    TimeCardRequired: Optional[CustomField]  # Made optional
    NoteID: Optional[CustomField]  # Made optional
    PrepaymentAcctID: Optional[CustomField]  # Made optional
    PrepaymentSubID: Optional[CustomField]  # Made optional
    ExpenseAcctID: Optional[CustomField]  # Made optional
    ExpenseSubID: Optional[CustomField]  # Made optional
    SalesAcctID: Optional[CustomField]  # Made optional
    SalesSubID: Optional[CustomField]  # Made optional
    TermsID: Optional[CustomField]  # Made optional

class EmployeeData(BaseModel):
    id: Optional[str]  # Made optional
    rowNumber: Optional[int]  # Made optional
    note: Optional[str]  # Made optional
    BranchID: Optional[Dict]  # Made optional
    Contact: Optional[Dict]  # Made optional
    CurrencyID: Optional[Dict]  # Made optional
    DateOfBirth: Optional[Dict]  # Made optional
    DepartmentID: Optional[Dict]  # Made optional
    EmployeeClassID: Optional[Dict]  # Made optional
    EmployeeCost: Optional[List[Dict]]  # Made optional
    EmployeeID: Optional[Dict]  # Made optional
    EmploymentHistory: Optional[List[EmploymentHistory]]  # Made optional
    Name: Optional[Dict]  # Made optional
    PaymentMethod: Optional[Dict]  # Made optional
    ReportsToID: Optional[Dict]  # Made optional
    Status: Optional[Dict]  # Made optional
    custom: Optional[CurrentEmployee]  # Made optional

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

            # Create EmployeeData while ignoring missing required fields
            return EmployeeData(**{k: v for k, v in employee_data.items() if v is not None})  # Only include non-None fields
        
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

    except ValidationError as e:
        # Handle validation errors and provide detailed feedback
        missing_fields = [error['loc'][-1] for error in e.errors() if error['type'] == 'value_error.missing']
        if missing_fields:
            detail_message = f"Missing required fields: {', '.join(missing_fields)}"
            raise HTTPException(status_code=422, detail=detail_message)
        raise HTTPException(status_code=422, detail="Validation error")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Log any unexpected exceptions
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
