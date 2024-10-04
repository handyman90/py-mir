# employee_get.py

from fastapi import FastAPI, HTTPException, Header
import requests
import json
import os
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Get the script name dynamically and create a corresponding JSON file name
script_name = os.path.splitext(os.path.basename(__file__))[0]  # Get the script name without extension
json_file_name = f"{script_name}.json"  # Create the JSON file name (e.g., employee_get.json)

# Load the JSON file (employee data)
try:
    with open(json_file_name, 'r') as file:
        employee_data = json.load(file)
except FileNotFoundError:
    employee_data = []  # Initialize an empty list if the JSON file doesn't exist

# Token URL and payload for authentication
token_url = "http://202.75.55.71/2023R1Preprod/identity/connect/token"

# Function to authenticate and get a session token
def get_auth_token():
    # Define the payload for authentication (raw payload converted to a dictionary)
    payload = {
        "grant_type": "password",
        "client_id": "03407458-3136-511B-24FB-68D470104D22@MIROS 090624",
        "client_secret": "3gVM0RbnqDwXYfO1aekAyw",
        "scope": "api",
        "username": "apiuser",
        "password": "apiuser"
    }

    # Set headers for the request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Make the POST request to get the token
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        # Extract the token from the response
        token = response.json().get('access_token')
        return token
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

# Define the data model for the employee response
class EmployeeGetModel(BaseModel):
    EmployeeID: str
    Name: str
    BranchID: str
    CurrencyID: str
    DateOfBirth: str
    DepartmentID: str
    EmployeeClassID: str
    PaymentMethod: str
    ReportsToID: str
    Status: bool

# Endpoint to retrieve employee information
@app.get("/organization/employee", response_model=EmployeeGetModel)
def get_employee(employee_id: str, authorization: str = Header(None)):
    if authorization is None:
        authorization = get_auth_token()

    # External API URL to fetch employee information
    url = f"http://202.75.55.71/2023R1Preprod/entity/GRP9Default/1/Employee?$filter=EmployeeID eq '{employee_id}'"
    headers = {"Authorization": f"Bearer {authorization}"}

    # Try to fetch employee data from the external API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return EmployeeGetModel(**data)  # Unpack the JSON response into the model
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
