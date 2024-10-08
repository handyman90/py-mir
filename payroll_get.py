# payroll_get.py

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
    value: Optional[str]  # Made optional

class ContactInfo(BaseModel):
    DateOfBirth: CustomField  # Required
    Email: Optional[CustomField]
    Fax: Optional[CustomField]
    FaxType: Optional[CustomField]
    FirstName: CustomField  # Required
    IdentityNumber: CustomField  # Required
    IdentityType: CustomField  # Required
    LastName: CustomField  # Required
    MiddleName: Optional[CustomField]
    Phone1: Optional[CustomField]
    Phone1Type: Optional[CustomField]
    Phone2: Optional[CustomField]
    Phone2Type: Optional[CustomField]
    Phone3: Optional[CustomField]
    Phone3Type: Optional[CustomField]
    Title: Optional[CustomField]

class EmploymentHistory(BaseModel):
    Active: CustomField  # Required
    EndDate: Optional[CustomField]
    LineNbr: CustomField  # Required
    PositionID: CustomField  # Required
    RehireEligible: CustomField  # Required
    StartDate: CustomField  # Required
    StartReason: CustomField  # Required
    Terminated: Optional[CustomField]
    TerminationReason: Optional[CustomField]
    custom: Optional[Dict]
    files: Optional[List[Dict]]

class EmployeeSettings(BaseModel):
    BranchID: CustomField  # Required
    Calendar: Optional[CustomField]
    CurrencyID: Optional[CustomField]
    CurrencyRateTypeID: Optional[CustomField]
    DepartmentID: CustomField  # Required
    EmployeeClass: CustomField  # Required
    EmployeeRefNbr: Optional[CustomField]
    EnableCurrencyOverride: Optional[CustomField]
    EnableRateOverride: Optional[CustomField]
    LaborItem: Optional[CustomField]
    RegularHoursValidation: Optional[CustomField]
    ReportsTo: Optional[CustomField]
    RouteEmails: Optional[CustomField]
    Salesperson: Optional[CustomField]
    TimeCardIsRequired: Optional[CustomField]

class FinancialSettings(BaseModel):
    APAccount: CustomField  # Required
    APSubaccount: CustomField  # Required
    CashAccount: CustomField  # Required
    ExpenseAccount: CustomField  # Required
    ExpenseSubaccount: CustomField  # Required
    PaymentMethod: CustomField  # Required
    PaymentInstructions: Optional[Dict]  # Adjust based on your structure
    PrepaymentAccount: Optional[CustomField]
    PrepaymentSubaccount: Optional[CustomField]
    SalesAccount: CustomField  # Required
    SalesSubaccount: CustomField  # Required
    TaxZone: Optional[CustomField]
    Terms: Optional[CustomField]

class PayrollData(BaseModel):
    EmployeeID: CustomField  # Required
    EmployeeName: CustomField  # Optional
    Status: CustomField  # Optional
    ContactInfo: ContactInfo  # Required
    EmploymentHistory: List[EmploymentHistory]  # Required
    EmployeeSettings: EmployeeSettings  # Required
    FinancialSettings: FinancialSettings  # Required

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

# Endpoint to retrieve payroll information
@app.get("/organization/payroll", response_model=List[PayrollData])
def get_payroll(employee_id: str, authorization: Optional[str] = Header(None)):
    try:
        # If no authorization token is provided in the header, get a new token
        if authorization is None:
            token_response = get_auth_token()  # Retrieve a new token
            authorization = token_response.get("access_token")  # Use the access_token

        # External API URL to fetch payroll information
        url = "http://202.75.55.71/2023R1Preprod/entity/GRP9Default/1/Payroll"

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

        # Fetch payroll data from the external API
        response = requests.get(url, headers=headers, params=payload)  # Pass payload as query parameters

        # Log the response status code and content
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            payroll_data = response.json()

            # Check if the response is a list of dictionaries
            if isinstance(payroll_data, list):
                return [PayrollData(**item) for item in payroll_data]  # Return list of payroll data
            else:
                raise HTTPException(status_code=500, detail="Unexpected response format")

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
