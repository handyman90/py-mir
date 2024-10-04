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
    type: str = ''  # Default to empty string
    value: Optional[str] = None  # Default to None

class Address(BaseModel):
    id: str = ''  # Default to empty string
    rowNumber: int = 0  # Default to 0
    note: Optional[str] = None  # Default to None
    AddressLine1: Dict[str, str] = {}  # Default to empty dict with string values
    AddressLine2: Dict[str, str] = {}  # Default to empty dict with string values
    City: Dict[str, str] = {}  # Default to empty dict with string values
    Country: Dict[str, str] = {}  # Default to empty dict with string values
    PostalCode: Dict[str, str] = {}  # Default to empty dict with string values
    State: Dict[str, str] = {}  # Default to empty dict with string values
    custom: Dict[str, str] = {}  # Default to empty dict with string values

class EmploymentHistory(BaseModel):
    id: str = ''  # Default to empty string
    rowNumber: int = 0  # Default to 0
    note: Optional[str] = None  # Default to None
    Active: Dict[str, str] = {}
    EndDate: Dict[str, str] = {}
    LineNbr: Dict[str, str] = {}
    PositionID: Dict[str, str] = {}
    RehireEligible: Dict[str, str] = {}
    StartDate: Dict[str, str] = {}
    StartReason: Dict[str, str] = {}
    Terminated: Dict[str, str] = {}
    TerminationReason: Dict[str, str] = {}
    custom: Dict[str, str] = {}

class CurrentEmployee(BaseModel):
    AcctReferenceNbr: CustomField = CustomField()
    UsrPlacementID: CustomField = CustomField()
    CalendarID: CustomField = CustomField()
    HoursValidation: CustomField = CustomField()
    SalesPersonID: CustomField = CustomField()
    UserID: CustomField = CustomField()
    AllowOverrideCury: CustomField = CustomField()
    CuryRateTypeID: CustomField = CustomField()
    AllowOverrideRate: CustomField = CustomField()
    LabourItemID: CustomField = CustomField()
    UnionID: CustomField = CustomField()
    RouteEmails: CustomField = CustomField()
    TimeCardRequired: CustomField = CustomField()
    NoteID: CustomField = CustomField()
    PrepaymentAcctID: CustomField = CustomField()
    PrepaymentSubID: CustomField = CustomField()
    ExpenseAcctID: CustomField = CustomField()
    ExpenseSubID: CustomField = CustomField()
    SalesAcctID: CustomField = CustomField()
    SalesSubID: CustomField = CustomField()
    TermsID: CustomField = CustomField()

class EmployeeData(BaseModel):
    id: str = ''  # Default to empty string
    rowNumber: int = 0  # Default to 0
    note: Optional[str] = None  # Default to None
    BranchID: Dict[str, str] = {}
    Contact: Dict[str, str] = {}  # Adjust this based on the exact structure of Contact
    CurrencyID: Dict[str, str] = {}
    DateOfBirth: Dict[str, str] = {}
    DepartmentID: Dict[str, str] = {}
    EmployeeClassID: Dict[str, str] = {}
    EmployeeCost: List[Dict] = []  # Default to an empty list
    EmployeeID: Dict[str, str] = {}
    EmploymentHistory: List[EmploymentHistory] = []  # Default to an empty list
    Name: Dict[str, str] = {}
    PaymentMethod: Dict[str, str] = {}
    ReportsToID: Dict[str, str] = {}
    Status: Dict[str, str] = {}
    custom: CurrentEmployee = CurrentEmployee()  # Default to an empty CurrentEmployee

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

    except ValidationError as e:
        # Handle missing fields gracefully
        raise HTTPException(status_code=422, detail=f"Validation error: {e.errors()}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Log any unexpected exceptions
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
