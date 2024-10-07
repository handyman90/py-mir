from fastapi import FastAPI, HTTPException, Depends
import requests
from sqlalchemy.orm import Session
from employee_put_models import Employee, EmployeePutModel  # Import models from employee_put_models.py
from models import SessionLocal  # Import the session for DB connection
from typing import Dict, Any
from datetime import datetime

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
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mapping between your database fields and API fields
FIELD_MAPPING = {
    "Nokt": "EmployeeID",      # Replace with actual API field if needed
    "Nama": "Name",            # Replace with actual API field if needed
    "Nokpbaru": "IdentityNumber",       # Placeholder for API field
    "tkhLahir": "DateOfBirth", # Replace with actual API field if needed
    # Add other mappings here...
}

# Function to map database fields to API fields
def map_fields_to_api(employee: Employee):
    employee_data = {}
    for db_field, api_field in FIELD_MAPPING.items():
        value = getattr(employee, db_field, None)
        if isinstance(value, datetime):
            value = value.isoformat()  # Format datetime values
        employee_data[api_field] = {"value": value}
    return employee_data

# Fetch employee from the database and send PUT request to the remote server
@app.put("/organization/employee/{employee_id}")
def update_employee_to_remote(employee_id: str, db: Session = Depends(get_db)):
    try:
        # Fetch employee from the peribadi_GRP table
        employee = db.query(Employee).filter(Employee.Nokt == employee_id).first()

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Map the database fields to the API fields
        employee_data = map_fields_to_api(employee)

        # Get authentication token
        access_token = get_auth_token()

        # Send PUT request to the remote server
        remote_url = f"http://202.75.55.71/2023R1Preprod/entity/GRP9Default/1/Employee/{employee_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.put(remote_url, json=employee_data, headers=headers)

        if response.status_code == 200:
            return {"message": "Employee data updated successfully on remote server."}
        elif response.status_code == 400:
            return {"message": "Bad Request", "details": response.json()}
        elif response.status_code == 500:
            return {"message": "Server error on remote server", "details": response.json()}
        else:
            response.raise_for_status()

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
