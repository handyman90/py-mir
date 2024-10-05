from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models import Employee, SessionLocal
from datetime import datetime

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

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class Address(BaseModel):
    id: Optional[str] = None
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    AddressLine1: Optional[Dict[str, Any]] = None
    AddressLine2: Optional[Dict[str, Any]] = None
    City: Optional[Dict[str, Any]] = None
    Country: Optional[Dict[str, Any]] = None
    PostalCode: Optional[Dict[str, Any]] = None
    State: Optional[Dict[str, Any]] = None
    custom: Optional[Dict[str, Any]] = None

class Contact(BaseModel):
    id: Optional[str] = None
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    Email: Optional[str] = None  # Using str for email
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Phone1: Optional[str] = None
    Phone2: Optional[str] = None
    Title: Optional[str] = None
    Address: Optional[Address] = None

class EmployeeResponse(BaseModel):
    employee_id: str
    row_number: Optional[int] = None
    note: Optional[str] = None
    branch_id: Optional[str] = None
    contact: Contact
    currency_id: Optional[str] = None
    date_of_birth: Optional[str] = None  # Or use datetime if you want to handle it as a date
    department_id: Optional[str] = None
    employee_class_id: Optional[str] = None
    employee_cost: Optional[List[Dict[str, Any]]] = None
    employment_history: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

# Endpoint to retrieve and save employee information
@app.get("/organization/employee", response_model=EmployeeResponse)
def get_employee(employee_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    try:
        if authorization is None:
            token_response = get_auth_token()
            authorization = token_response.get("access_token")

        url = "http://202.75.55.71/2023R1Preprod/entity/GRP9Default/1/Employee"
        headers = {"Authorization": f"Bearer {authorization}"}
        params = {"$filter": f"EmployeeID eq '{employee_id}'"}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            employee_data = response.json()
            employee_data = employee_data[0]  # Extract first record if it's a list

            # Check if employee exists in the DB, otherwise add a new one
            existing_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
            
            if existing_employee:
                # Update existing employee with fields from employee_data
                existing_employee.row_number = employee_data.get("rowNumber")
                existing_employee.note = employee_data.get("note")
                existing_employee.branch_id = employee_data.get("BranchID", {}).get("id")
                existing_employee.contact_id = employee_data.get("Contact", {}).get("id")
                existing_employee.currency_id = employee_data.get("CurrencyID", {}).get("id")
                existing_employee.date_of_birth = datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00").split("+")[0])
                existing_employee.department_id = employee_data.get("DepartmentID", {}).get("id")
                existing_employee.employee_class_id = employee_data.get("EmployeeClassID", {}).get("id")
                existing_employee.employee_cost = employee_data.get("EmployeeCost", [])
                existing_employee.employment_history = employee_data.get("EmploymentHistory", [])
                existing_employee.status = employee_data.get("Status", {}).get("value")
                existing_employee.custom_fields = employee_data.get("custom")

            else:
                # Create a new employee record
                employee = Employee(
                    employee_id=employee_data.get("EmployeeID", {}).get("value"),
                    row_number=employee_data.get("rowNumber"),
                    note=employee_data.get("note"),
                    branch_id=employee_data.get("BranchID", {}).get("id"),
                    contact_id=employee_data.get("Contact", {}).get("id"),
                    currency_id=employee_data.get("CurrencyID", {}).get("id"),
                    date_of_birth=datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00").split("+")[0]),
                    department_id=employee_data.get("DepartmentID", {}).get("id"),
                    employee_class_id=employee_data.get("EmployeeClassID", {}).get("id"),
                    employee_cost=employee_data.get("EmployeeCost", []),
                    employment_history=employee_data.get("EmploymentHistory", []),
                    status=employee_data.get("Status", {}).get("value"),
                    custom_fields=employee_data.get("custom")
                )
                db.add(employee)

            db.commit()
            return EmployeeResponse(
                employee_id=existing_employee.employee_id if existing_employee else employee.employee_id,
                row_number=existing_employee.row_number if existing_employee else employee.row_number,
                note=existing_employee.note if existing_employee else employee.note,
                branch_id=existing_employee.branch_id if existing_employee else employee.branch_id,
                contact=Contact(
                    id=existing_employee.contact_id if existing_employee else employee.contact_id,
                    rowNumber=existing_employee.row_number if existing_employee else employee.row_number,
                    note=existing_employee.note if existing_employee else employee.note,
                    Email=existing_employee.contact_email if existing_employee else employee.contact_email,
                    FirstName=existing_employee.contact_first_name if existing_employee else employee.contact_first_name,
                    LastName=existing_employee.contact_last_name if existing_employee else employee.contact_last_name,
                    Phone1=existing_employee.contact_phone1 if existing_employee else employee.contact_phone1,
                    Phone2=existing_employee.contact_phone2 if existing_employee else employee.contact_phone2,
                    Title=existing_employee.contact_title if existing_employee else employee.contact_title,
                    Address=None  # Assuming you'll handle addresses separately
                ),
                currency_id=existing_employee.currency_id if existing_employee else employee.currency_id,
                date_of_birth=existing_employee.date_of_birth.strftime("%Y-%m-%d") if existing_employee else employee.date_of_birth.strftime("%Y-%m-%d"),  # Convert to string
                department_id=existing_employee.department_id if existing_employee else employee.department_id,
                employee_class_id=existing_employee.employee_class_id if existing_employee else employee.employee_class_id,
                employee_cost=existing_employee.employee_cost if existing_employee else employee.employee_cost,
                employment_history=existing_employee.employment_history if existing_employee else employee.employment_history,
                status=existing_employee.status if existing_employee else employee.status,
                custom_fields=existing_employee.custom_fields if existing_employee else employee.custom_fields,
            )

        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
