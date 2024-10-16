from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from sqlalchemy.orm import Session
from employee_get_models import EmployeeResponse  # Ensure this imports the updated model
from models import Employee, SessionLocal
from datetime import datetime

app = FastAPI()

# Function to authenticate and get a session token
def get_auth_token() -> dict:
    token_url = "https://csmstg.censof.com/2023R1Preprod/identity/connect/token"
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

# Function to save employee data to the database
def save_employee_to_db(db: Session, employee_data: EmployeeResponse):
    existing_employee = db.query(Employee).filter(Employee.employee_id == employee_data.EmployeeID["value"]).first()

    if existing_employee:
        # Update existing employee record
        existing_employee.row_number = employee_data.rowNumber
        existing_employee.note = employee_data.note
        existing_employee.branch_id = employee_data.BranchID["value"]
        existing_employee.currency_id = employee_data.CurrencyID["value"]
        existing_employee.date_of_birth = datetime.fromisoformat(employee_data.DateOfBirth["value"].replace("Z", "+00:00"))
        existing_employee.department_id = employee_data.DepartmentID["value"]
        existing_employee.employee_class_id = employee_data.EmployeeClassID["value"]
        existing_employee.name = employee_data.Name["value"]
        existing_employee.payment_method = employee_data.PaymentMethod["value"]
        existing_employee.status = employee_data.Status["value"]
    else:
        # Insert new employee record
        new_employee = Employee(
            employee_id=employee_data.EmployeeID["value"],
            row_number=employee_data.rowNumber,
            note=employee_data.note,
            branch_id=employee_data.BranchID["value"],
            currency_id=employee_data.CurrencyID["value"],
            date_of_birth=datetime.fromisoformat(employee_data.DateOfBirth["value"].replace("Z", "+00:00")),
            department_id=employee_data.DepartmentID["value"],
            employee_class_id=employee_data.EmployeeClassID["value"],
            name=employee_data.Name["value"],
            payment_method=employee_data.PaymentMethod["value"],
            status=employee_data.Status["value"],
        )
        db.add(new_employee)

    db.commit()

# Endpoint to retrieve and save employee information
@app.get("/organization/employee", response_model=EmployeeResponse)
def get_employee(employee_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    try:
        if authorization is None:
            token_response = get_auth_token()
            authorization = token_response.get("access_token")

        # Updated URL for retrieving employee data
        url = f"https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee/{employee_id}?$expand=Contact/Address,EmploymentHistory,PaymentInstruction"
        headers = {"Authorization": f"Bearer {authorization}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            employee_data = response.json()  # Get the response data
            employee_response = EmployeeResponse(**employee_data)

            # Save employee data to the database
            save_employee_to_db(db, employee_response)

            return employee_response
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
