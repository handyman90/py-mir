from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from sqlalchemy.orm import Session
from models import SessionLocal, Employee
from employee_get_models import EmployeeResponse
from datetime import datetime
from typing import Optional

app = FastAPI()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to authenticate and get a session token
def get_auth_token():
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

# Endpoint to retrieve and save employee information
@app.get("/organization/employee/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: str, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if authorization is None:
        token_response = get_auth_token()
        authorization = token_response.get("access_token")

    url = f"https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee/{employee_id}?$expand=Contact/Address,EmploymentHistory,PaymentInstruction"
    headers = {"Authorization": f"Bearer {authorization}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        employee_data = response.json()

        # Flatten nested fields and create a new employee object or update an existing one
        employee = Employee(
            id=employee_data["id"],
            row_number=employee_data.get("rowNumber"),
            note=employee_data.get("note"),
            BranchID=employee_data["BranchID"]["value"],
            Calendar=employee_data["Calendar"]["value"],
            CashAccount=employee_data["CashAccount"]["value"],
            ContactID=employee_data["Contact"]["id"],
            ContactRowNumber=employee_data["Contact"]["rowNumber"],
            ContactNote=employee_data["Contact"].get("note"),
            ContactDisplayName=employee_data["Contact"]["DisplayName"]["value"],
            ContactEmail=employee_data["Contact"]["Email"]["value"],
            ContactFax=employee_data["Contact"].get("Fax"),
            ContactFirstName=employee_data["Contact"].get("FirstName"),
            ContactLastName=employee_data["Contact"]["LastName"]["value"],
            ContactMiddleName=employee_data["Contact"].get("MiddleName"),
            ContactPhone1=employee_data["Contact"].get("Phone1"),
            ContactPhone1Type=employee_data["Contact"]["Phone1Type"]["value"],
            ContactPhone2=employee_data["Contact"].get("Phone2"),
            ContactPhone2Type=employee_data["Contact"]["Phone2Type"]["value"],
            ContactTitle=employee_data["Contact"]["Title"]["value"],
            CurrencyID=employee_data["CurrencyID"]["value"],
            DateOfBirth=datetime.fromisoformat(employee_data["DateOfBirth"]["value"].replace("Z", "+00:00")),
            DepartmentID=employee_data["DepartmentID"]["value"],
            EmployeeClassID=employee_data["EmployeeClassID"]["value"],
            EmployeeID=employee_data["EmployeeID"]["value"],
            EmploymentHistoryID=employee_data["EmploymentHistory"][0]["id"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryRowNumber=employee_data["EmploymentHistory"][0]["rowNumber"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryNote=employee_data["EmploymentHistory"][0].get("note"),
            EmploymentHistoryActive=employee_data["EmploymentHistory"][0]["Active"]["value"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryEndDate=employee_data["EmploymentHistory"][0].get("EndDate"),
            EmploymentHistoryLineNbr=employee_data["EmploymentHistory"][0]["LineNbr"]["value"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryPositionID=employee_data["EmploymentHistory"][0]["PositionID"]["value"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryRehireEligible=employee_data["EmploymentHistory"][0]["RehireEligible"]["value"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryStartDate=employee_data["EmploymentHistory"][0]["StartDate"]["value"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryStartReason=employee_data["EmploymentHistory"][0]["StartReason"]["value"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryTerminated=employee_data["EmploymentHistory"][0]["Terminated"]["value"] if employee_data["EmploymentHistory"] else None,
            EmploymentHistoryTerminationReason=employee_data["EmploymentHistory"][0].get("TerminationReason"),
            ExpenseAccount=employee_data["ExpenseAccount"]["value"],
            ExpenseSubaccount=employee_data["ExpenseSubaccount"]["value"],
            IdentityNumber=employee_data["IdentityNumber"]["value"],
            IdentityType=employee_data["IdentityType"]["value"],
            LastModifiedDateTime=datetime.fromisoformat(employee_data["LastModifiedDateTime"]["value"].replace("Z", "+00:00")),
            Name=employee_data["Name"]["value"],
            PaymentInstructionID=employee_data["PaymentInstruction"][0]["id"] if employee_data["PaymentInstruction"] else None,
            PaymentInstructionRowNumber=employee_data["PaymentInstruction"][0]["rowNumber"] if employee_data["PaymentInstruction"] else None,
            PaymentInstructionNote=employee_data["PaymentInstruction"][0].get("note"),
            PaymentInstructionBAccountID=employee_data["PaymentInstruction"][0]["BAccountID"]["value"] if employee_data["PaymentInstruction"] else None,
            PaymentInstructionDescription=employee_data["PaymentInstruction"][0]["Description"]["value"] if employee_data["PaymentInstruction"] else None,
            PaymentInstructionInstructionID=employee_data["PaymentInstruction"][0]["InstructionID"]["value"] if employee_data["PaymentInstruction"] else None,
            PaymentInstructionLocationID=employee_data["PaymentInstruction"][0]["LocationID"]["value"] if employee_data["PaymentInstruction"] else None,
            PaymentMethod=employee_data["PaymentMethod"]["value"],
            ReportsToID=employee_data.get("ReportsToID"),
            SalesAccount=employee_data["SalesAccount"]["value"],
            SalesSubaccount=employee_data["SalesSubaccount"]["value"],
            Status=employee_data["Status"]["value"],
            custom=employee_data.get("custom"),
            links=employee_data.get("_links")
        )

        db.add(employee)
        db.commit()
        return employee

    else:
        print(f"Error fetching data for Employee ID {employee_id}: {response.status_code}, {response.json()}")
        raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
