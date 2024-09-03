from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

# Define the PUT data model based on fields from pages 50-51
class PayrollEmployeePut(BaseModel):
    EmployeeID: Optional[str]  # String
    EmployeeName: Optional[str]  # String
    PayrollID: Optional[str]  # String
    PayGroup: Optional[str]  # String
    DepartmentID: Optional[str]  # String
    PositionID: Optional[str]  # String
    EmploymentType: Optional[str]  # String
    PayType: Optional[str]  # String
    PayFrequency: Optional[str]  # String
    BasicSalary: Optional[float]  # Float
    Allowances: Optional[float]  # Float
    Deductions: Optional[float]  # Float
    NetPay: Optional[float]  # Float
    LastModifiedDateTime: Optional[str]  # String (DateTime)
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

# Endpoint to insert or update payroll employee information
@app.put("/organization/payroll_employee", response_model=PayrollEmployeePut)
def insert_payroll_employee(employee: PayrollEmployeePut, authorization: str = Header(None)):
    if authorization is None:
        authorization = get_auth_token()

    url = "https://example.com/entity/GRP9Default/1/PayrollEmployee"
    headers = {"Authorization": authorization}
    payload = employee.dict()

    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 200:
        return employee
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
