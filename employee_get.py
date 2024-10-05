from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from pydantic import BaseModel
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from models import Employee, SessionLocal

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

# Define Pydantic models according to the expected JSON structure
class CustomField(BaseModel):
    type: Optional[str]  
    value: Optional[str]  

class Address(BaseModel):
    id: Optional[str]  
    rowNumber: Optional[int]  
    note: Optional[str]  
    AddressLine1: Optional[Dict]  
    AddressLine2: Optional[Dict]  
    City: Optional[Dict]  
    Country: Optional[Dict]  
    PostalCode: Optional[Dict]  
    State: Optional[Dict]  
    custom: Optional[Dict]  

class EmploymentHistory(BaseModel):
    id: Optional[str]  
    rowNumber: Optional[int]  
    note: Optional[str]  
    Active: Optional[Dict]  
    EndDate: Optional[Dict]  
    LineNbr: Optional[Dict]  
    PositionID: Optional[Dict]  
    RehireEligible: Optional[Dict]  
    StartDate: Optional[Dict]  
    StartReason: Optional[Dict]  
    Terminated: Optional[Dict]  
    TerminationReason: Optional[Dict]  
    custom: Optional[Dict]  

class CurrentEmployee(BaseModel):
    AcctReferenceNbr: Optional[CustomField]  
    UsrPlacementID: Optional[CustomField]  
    CalendarID: Optional[CustomField]  
    HoursValidation: Optional[CustomField]  
    SalesPersonID: Optional[CustomField]  
    UserID: Optional[CustomField]  
    AllowOverrideCury: Optional[CustomField]  
    CuryRateTypeID: Optional[CustomField]  
    AllowOverrideRate: Optional[CustomField]  
    LabourItemID: Optional[CustomField]  
    UnionID: Optional[CustomField]  
    RouteEmails: Optional[CustomField]  
    TimeCardRequired: Optional[CustomField]  
    NoteID: Optional[CustomField]  
    PrepaymentAcctID: Optional[CustomField]  
    PrepaymentSubID: Optional[CustomField]  
    ExpenseAcctID: Optional[CustomField]  
    ExpenseSubID: Optional[CustomField]  
    SalesAcctID: Optional[CustomField]  
    SalesSubID: Optional[CustomField]  
    TermsID: Optional[CustomField]  

class EmployeeData(BaseModel):
    id: Optional[str]  
    rowNumber: Optional[int]  
    note: Optional[str]  
    BranchID: Optional[Dict]  
    Contact: Optional[Dict]  
    CurrencyID: Optional[Dict]  
    DateOfBirth: Optional[Dict]  
    DepartmentID: Optional[Dict]  
    EmployeeClassID: Optional[Dict]  
    EmployeeCost: Optional[List[Dict]]  
    EmployeeID: Optional[Dict]  
    EmploymentHistory: Optional[List[EmploymentHistory]]  
    Name: Optional[Dict]  
    PaymentMethod: Optional[Dict]  
    ReportsToID: Optional[Dict]  
    Status: Optional[Dict]  
    custom: Optional[CurrentEmployee]  

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to test the token
@app.get("/test-token", response_model=dict)
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

# Endpoint to retrieve and save employee information
@app.get("/organization/employee", response_model=EmployeeData)
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
                existing_employee.branch_id = employee_data.get("BranchID", {}).get("id")  # Assuming BranchID contains an ID
                existing_employee.contact_id = employee_data.get("Contact", {}).get("id")  # Assuming Contact has its own ID
                existing_employee.currency_id = employee_data.get("CurrencyID", {}).get("id")  # Assuming CurrencyID has its own ID
                existing_employee.date_of_birth = employee_data.get("DateOfBirth", {}).get("value")
                existing_employee.department_id = employee_data.get("DepartmentID", {}).get("id")  # Assuming DepartmentID has its own ID
                existing_employee.employee_class_id = employee_data.get("EmployeeClassID", {}).get("id")  # Assuming EmployeeClassID has its own ID
                existing_employee.employee_cost = employee_data.get("EmployeeCost", [])
                existing_employee.employment_history = employee_data.get("EmploymentHistory", [])
                existing_employee.status = employee_data.get("Status", {}).get("value")
                existing_employee.custom = employee_data.get("custom")  # Storing entire custom field

            else:
                # Create a new employee record
                employee = Employee(
                    employee_id=employee_data.get("EmployeeID", {}).get("value"),
                    row_number=employee_data.get("rowNumber"),
                    note=employee_data.get("note"),
                    branch_id=employee_data.get("BranchID", {}).get("id"),
                    contact_id=employee_data.get("Contact", {}).get("id"),
                    currency_id=employee_data.get("CurrencyID", {}).get("id"),
                    date_of_birth=employee_data.get("DateOfBirth", {}).get("value"),
                    department_id=employee_data.get("DepartmentID", {}).get("id"),
                    employee_class_id=employee_data.get("EmployeeClassID", {}).get("id"),
                    employee_cost=employee_data.get("EmployeeCost", []),
                    employment_history=employee_data.get("EmploymentHistory", []),
                    status=employee_data.get("Status", {}).get("value"),
                    custom=employee_data.get("custom")  # Storing entire custom field
                )
                db.add(employee)

            db.commit()
            return EmployeeData(
                id=employee.employee_id,
                rowNumber=employee.row_number,
                note=employee.note,
                BranchID={"id": existing_employee.branch_id},  # Assuming you return the ID in a dict format
                Contact={"id": existing_employee.contact_id},  # Return the contact in the same way
                CurrencyID={"id": existing_employee.currency_id},
                DateOfBirth={"value": existing_employee.date_of_birth},
                DepartmentID={"id": existing_employee.department_id},
                EmployeeClassID={"id": existing_employee.employee_class_id},
                EmployeeCost=existing_employee.employee_cost,
                EmployeeID={"value": existing_employee.employee_id},
                EmploymentHistory=existing_employee.employment_history,
                Name={},
                PaymentMethod={},
                ReportsToID={},
                Status={"value": existing_employee.status},
                custom=existing_employee.custom
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
