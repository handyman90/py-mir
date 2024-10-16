from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from models import Employee, Contact, Address, EmploymentHistory, PaymentInstruction, SessionLocal
from datetime import datetime

app = FastAPI()

# Token URL and payload for authentication
token_url = "https://csmstg.censof.com/2023R1Preprod/identity/connect/token"

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

# Pydantic models for response structure
class ValueField(BaseModel):
    value: Optional[str]  # Make value optional

class AddressModel(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: ValueField
    AddressLine2: ValueField
    City: Optional[Dict[str, Any]] = None
    Country: ValueField
    PostalCode: Optional[Dict[str, Any]] = None
    State: Optional[Dict[str, Any]] = None
    custom: Optional[Dict[str, Any]] = None
    files: Optional[List] = None

class ContactModel(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Address: AddressModel
    DisplayName: ValueField
    Email: ValueField
    Fax: Optional[Dict[str, Any]] = None
    FirstName: Optional[Dict[str, Any]] = None
    LastName: ValueField
    MiddleName: Optional[Dict[str, Any]] = None
    Phone1: Optional[Dict[str, Any]] = None
    Phone1Type: ValueField
    Phone2: Optional[Dict[str, Any]] = None
    Phone2Type: ValueField
    Title: ValueField
    custom: Optional[Dict[str, Any]] = None
    files: Optional[List] = None

class EmploymentHistoryModel(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: ValueField
    EndDate: Optional[Dict[str, Any]] = None
    LineNbr: ValueField
    PositionID: ValueField
    RehireEligible: ValueField
    StartDate: ValueField
    StartReason: ValueField
    Terminated: ValueField
    TerminationReason: Optional[Dict[str, Any]] = None
    custom: Optional[Dict[str, Any]] = None
    _links: Optional[Dict[str, Any]] = None
    files: Optional[List] = None

class PaymentInstructionModel(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    BAccountID: ValueField
    Description: ValueField
    InstructionID: ValueField
    LocationID: ValueField
    PaymentMethod: ValueField
    Value: ValueField
    custom: Optional[Dict[str, Any]] = None
    files: Optional[List] = None

class EmployeeResponse(BaseModel):
    id: str
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    BranchID: ValueField
    Calendar: ValueField
    CashAccount: ValueField
    Contact: ContactModel
    CurrencyID: ValueField
    DateOfBirth: ValueField
    DepartmentID: ValueField
    EmployeeClassID: ValueField
    EmployeeID: ValueField
    EmploymentHistory: List[EmploymentHistoryModel]
    ExpenseAccount: ValueField
    ExpenseSubaccount: ValueField
    IdentityNumber: ValueField
    IdentityType: ValueField
    LastModifiedDateTime: ValueField
    Name: ValueField
    PaymentInstruction: List[PaymentInstructionModel]
    PaymentMethod: ValueField
    ReportsToID: Optional[Dict[str, Any]] = None
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict[str, Any]] = None
    links: Optional[Dict[str, Any]] = None
    files: Optional[List] = None

# Endpoint to retrieve and save employee information
@app.get("/organization/employee/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    try:
        if authorization is None:
            token_response = get_auth_token()
            authorization = token_response.get("access_token")

        url = f"https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee/{employee_id}?$expand=Contact/Address,EmploymentHistory,PaymentInstruction"
        headers = {"Authorization": f"Bearer {authorization}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            employee_data = response.json()

            # Create or update employee record in the database
            existing_employee = db.query(Employee).filter(Employee.employee_id == employee_data["EmployeeID"]["value"]).first()
            
            if existing_employee:
                # Update existing employee
                existing_employee.row_number = employee_data.get("rowNumber")
                existing_employee.note = employee_data.get("note", "")
                existing_employee.branch_id = employee_data.get("BranchID", {}).get("value")
                existing_employee.calendar = employee_data.get("Calendar", {}).get("value")
                existing_employee.cash_account = employee_data.get("CashAccount", {}).get("value")
                existing_employee.currency_id = employee_data.get("CurrencyID", {}).get("value")
                existing_employee.date_of_birth = datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00"))
                existing_employee.department_id = employee_data.get("DepartmentID", {}).get("value")
                existing_employee.employee_class_id = employee_data.get("EmployeeClassID", {}).get("value")
                existing_employee.expense_account = employee_data.get("ExpenseAccount", {}).get("value")
                existing_employee.expense_subaccount = employee_data.get("ExpenseSubaccount", {}).get("value")
                existing_employee.identity_number = employee_data.get("IdentityNumber", {}).get("value")
                existing_employee.identity_type = employee_data.get("IdentityType", {}).get("value")
                existing_employee.last_modified_date_time = datetime.fromisoformat(employee_data.get("LastModifiedDateTime", {}).get("value").replace("Z", "+00:00"))
                existing_employee.name = employee_data.get("Name", {}).get("value")
                existing_employee.payment_method = employee_data.get("PaymentMethod", {}).get("value")
                existing_employee.reports_to_id = employee_data.get("ReportsToID", {}).get("value")  
                existing_employee.sales_account = employee_data.get("SalesAccount", {}).get("value")
                existing_employee.sales_subaccount = employee_data.get("SalesSubaccount", {}).get("value")
                existing_employee.status = employee_data.get("Status", {}).get("value")
                existing_employee.custom_fields = employee_data.get("custom", {})
                
                # Update contact and related data here as well...
                
            else:
                # Create a new employee record
                employee = Employee(
                    employee_id=employee_data.get("EmployeeID", {}).get("value"),
                    row_number=employee_data.get("rowNumber"),
                    note=employee_data.get("note", ""),
                    branch_id=employee_data.get("BranchID", {}).get("value"),
                    calendar=employee_data.get("Calendar", {}).get("value"),
                    cash_account=employee_data.get("CashAccount", {}).get("value"),
                    currency_id=employee_data.get("CurrencyID", {}).get("value"),
                    date_of_birth=datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00")),
                    department_id=employee_data.get("DepartmentID", {}).get("value"),
                    employee_class_id=employee_data.get("EmployeeClassID", {}).get("value"),
                    expense_account=employee_data.get("ExpenseAccount", {}).get("value"),
                    expense_subaccount=employee_data.get("ExpenseSubaccount", {}).get("value"),
                    identity_number=employee_data.get("IdentityNumber", {}).get("value"),
                    identity_type=employee_data.get("IdentityType", {}).get("value"),
                    last_modified_date_time=datetime.fromisoformat(employee_data.get("LastModifiedDateTime", {}).get("value").replace("Z", "+00:00")),
                    name=employee_data.get("Name", {}).get("value"),
                    payment_method=employee_data.get("PaymentMethod", {}).get("value"),
                    reports_to_id=employee_data.get("ReportsToID", {}).get("value"),
                    sales_account=employee_data.get("SalesAccount", {}).get("value"),
                    sales_subaccount=employee_data.get("SalesSubaccount", {}).get("value"),
                    status=employee_data.get("Status", {}).get("value"),
                    custom_fields=employee_data.get("custom", {}),
                    links=employee_data.get("_links", {})
                )
                db.add(employee)

            db.commit()
            return EmployeeResponse(
                id=existing_employee.employee_id if existing_employee else employee.employee_id,
                rowNumber=existing_employee.row_number if existing_employee else employee.row_number,
                note=existing_employee.note if existing_employee else employee.note,
                BranchID={"value": existing_employee.branch_id} if existing_employee else {"value": employee.branch_id},
                Calendar={"value": existing_employee.calendar} if existing_employee else {"value": employee.calendar},
                CashAccount={"value": existing_employee.cash_account} if existing_employee else {"value": employee.cash_account},
                CurrencyID={"value": existing_employee.currency_id} if existing_employee else {"value": employee.currency_id},
                DateOfBirth={"value": existing_employee.date_of_birth.isoformat()} if existing_employee else {"value": employee.date_of_birth.isoformat()},
                DepartmentID={"value": existing_employee.department_id} if existing_employee else {"value": employee.department_id},
                EmployeeClassID={"value": existing_employee.employee_class_id} if existing_employee else {"value": employee.employee_class_id},
                EmployeeID={"value": existing_employee.employee_id} if existing_employee else {"value": employee.employee_id},
                ExpenseAccount={"value": existing_employee.expense_account} if existing_employee else {"value": employee.expense_account},
                ExpenseSubaccount={"value": existing_employee.expense_subaccount} if existing_employee else {"value": employee.expense_subaccount},
                IdentityNumber={"value": existing_employee.identity_number} if existing_employee else {"value": employee.identity_number},
                IdentityType={"value": existing_employee.identity_type} if existing_employee else {"value": employee.identity_type},
                LastModifiedDateTime={"value": existing_employee.last_modified_date_time.isoformat()} if existing_employee else {"value": employee.last_modified_date_time.isoformat()},
                Name={"value": existing_employee.name} if existing_employee else {"value": employee.name},
                PaymentMethod={"value": existing_employee.payment_method} if existing_employee else {"value": employee.payment_method},
                ReportsToID={},
                SalesAccount={"value": existing_employee.sales_account} if existing_employee else {"value": employee.sales_account},
                SalesSubaccount={"value": existing_employee.sales_subaccount} if existing_employee else {"value": employee.sales_subaccount},
                Status={"value": existing_employee.status} if existing_employee else {"value": employee.status},
                custom={},
                links=existing_employee.links if existing_employee else employee.links
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
