from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

# Define the GET data model based on common employee fields
class EmployeeGet(BaseModel):
    EmployeeID: Optional[str]  # String
    Name: Optional[str]  # String
    BranchID: Optional[str]  # String
    CurrencyID: Optional[str]  # String
    DateOfBirth: Optional[str]  # String (Date)
    DepartmentID: Optional[str]  # String
    EmployeeClassID: Optional[str]  # String
    PaymentMethod: Optional[str]  # String
    ReportsToID: Optional[str]  # String
    Status: Optional[bool]  # Boolean
    LastModifiedDateTime: Optional[str]  # String (DateTime)
    IdentityNumber: Optional[str]  # String
    IdentityType: Optional[str]  # String
    SalesAccount: Optional[str]  # String
    SalesSubaccount: Optional[str]  # String
    ExpenseAccount: Optional[str]  # String
    ExpenseSubaccount: Optional[str]  # String
    Calendar: Optional[str]  # String
    Country: Optional[str]  # String
    LastName: Optional[str]  # String
    Active: Optional[bool]  # Boolean
    AddressIsSameAsInAccount: Optional[bool]  # Boolean
    AddressValidated: Optional[bool]  # Boolean
    Attention: Optional[str]  # String
    BusinessAccount: Optional[str]  # String
    CompanyName: Optional[str]  # String
    # Add additional fields as needed

# Function to authenticate and get a session token
def get_auth_token():
    token_url = "https://example.com/entity/auth/login"
    payload = {
        "name": "admin",
        "password": "123",
        "company": "Company"
    }

    response = requests.post(token_url, json=payload)
    if response.status_code == 204:
        return response.headers['Authorization']
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")

# Endpoint to retrieve employee information
@app.get("/organization/employee", response_model=EmployeeGet)
def get_employee(employee_id: str, authorization: str = Header(None)):
    if authorization is None:
        authorization = get_auth_token()

    url = f"https://example.com/entity/GRP9Default/1/Employee?$filter=EmployeeID eq '{employee_id}'"
    headers = {"Authorization": authorization}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return EmployeeGet(**data)
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
