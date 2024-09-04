# payroll_get.py

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Any
import requests

app = FastAPI()

# Define a dynamic model for GET operations
class PayrollEmployeeGetModel(BaseModel):
    data: Dict[str, Any]

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

# Endpoint to retrieve payroll employee information
@app.get("/organization/payroll_employee", response_model=PayrollEmployeeGetModel)
def get_payroll_employee(employee_id: str, authorization: str = Header(None)):
    if authorization is None:
        authorization = get_auth_token()

    url = f"https://example.com/entity/GRP9Default/1/PayrollEmployee?$filter=EmployeeID eq '{employee_id}'"
    headers = {"Authorization": authorization}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return PayrollEmployeeGetModel(data=data)
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
