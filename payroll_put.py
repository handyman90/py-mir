# payroll_put.py

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Any
import requests

app = FastAPI()

# Define a dynamic model for PUT operations
class PayrollEmployeePutModel(BaseModel):
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

# Endpoint to insert or update payroll employee information
@app.put("/organization/payroll_employee", response_model=PayrollEmployeePutModel)
def put_payroll_employee(employee: PayrollEmployeePutModel, authorization: str = Header(None)):
    if authorization is None:
        authorization = get_auth_token()

    url = "https://example.com/entity/GRP9Default/1/PayrollEmployee"
    headers = {"Authorization": authorization}
    payload = employee.data

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
