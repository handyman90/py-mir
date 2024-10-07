from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from models import SessionLocal
from employee_get_models import Employee, EmployeeGetModel  # Import the SQLAlchemy model for GET operation
import requests
from typing import List

app = FastAPI()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# Endpoint to retrieve and save employee information
@app.get("/organization/employee", response_model=EmployeeGetModel)
def get_employee(employee_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    try:
        if authorization is None:
            authorization = get_auth_token()

        url = "http://202.75.55.71/2023R1Preprod/entity/GRP9Default/1/Employee"
        headers = {"Authorization": f"Bearer {authorization}"}
        params = {"$filter": f"EmployeeID eq '{employee_id}'"}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            employee_data = response.json()
            employee_data = employee_data[0]  # Extract first record if it's a list

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
                existing_employee.reports_to_id = employee_data.get("ReportsToID", {}).get("value")  # Assuming ReportsToID is also a value field
                existing_employee.sales_account = employee_data.get("SalesAccount", {}).get("value")
                existing_employee.sales_subaccount = employee_data.get("SalesSubaccount", {}).get("value")
                existing_employee.status = employee_data.get("Status", {}).get("value")
                existing_employee.custom_fields = employee_data.get("custom", {})
                existing_employee.links = employee_data.get("_links", {})

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
                _links=existing_employee.links if existing_employee else employee.links
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
