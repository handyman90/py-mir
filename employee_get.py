from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from sqlalchemy.orm import Session
from models import SessionLocal
from employee_get_models import EmployeeResponse, ValueField, Contact, Address, EmploymentHistory, PaymentInstruction
from typing import Optional
from datetime import datetime

app = FastAPI()

# Token URL
token_url = "https://csmstg.censof.com/2023R1Preprod/identity/connect/token"

# Function to authenticate and get a session token
def get_auth_token() -> str:
    payload = {
        "grant_type": "password",
        "client_id": "03407458-3136-511B-24FB-68D470104D22@MIROS 090624",
        "client_secret": "3gVM0RbnqDwXYfO1aekAyw",
        "scope": "api",
        "username": "apiuser",
        "password": "apiuser"  # Replace with your actual password
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to retrieve employee information
@app.get("/organization/employee/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: str, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    try:
        if authorization is None:
            token = get_auth_token()
            authorization = f"Bearer {token}"

        url = f"https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee/{employee_id}?$expand=Contact/Address,EmploymentHistory,PaymentInstruction"
        headers = {"Authorization": authorization}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            employee_data = response.json()

            # Flatten nested fields and create EmployeeResponse
            employee_response = EmployeeResponse(
                id=employee_data.get("id"),
                rowNumber=employee_data.get("rowNumber"),
                note=employee_data.get("note"),
                BranchID=ValueField(value=employee_data.get("BranchID", {}).get("value", None) if isinstance(employee_data.get("BranchID"), dict) else employee_data.get("BranchID")),
                Calendar=ValueField(value=employee_data.get("Calendar", {}).get("value", None) if isinstance(employee_data.get("Calendar"), dict) else employee_data.get("Calendar")),
                CashAccount=ValueField(value=employee_data.get("CashAccount", {}).get("value", None) if isinstance(employee_data.get("CashAccount"), dict) else employee_data.get("CashAccount")),
                Contact=Contact(
                    id=employee_data.get("Contact", {}).get("id", None),
                    rowNumber=employee_data.get("Contact", {}).get("rowNumber", None),
                    note=employee_data.get("Contact", {}).get("note", None),
                    DisplayName=ValueField(value=employee_data.get("Contact", {}).get("DisplayName", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("DisplayName"), dict) else employee_data.get("Contact", {}).get("DisplayName")),
                    Email=ValueField(value=employee_data.get("Contact", {}).get("Email", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("Email"), dict) else employee_data.get("Contact", {}).get("Email")),
                    Fax=ValueField(value=employee_data.get("Contact", {}).get("Fax", None)),
                    FirstName=ValueField(value=employee_data.get("Contact", {}).get("FirstName", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("FirstName"), dict) else employee_data.get("Contact", {}).get("FirstName")),
                    LastName=ValueField(value=employee_data.get("Contact", {}).get("LastName", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("LastName"), dict) else employee_data.get("Contact", {}).get("LastName")),
                    MiddleName=ValueField(value=employee_data.get("Contact", {}).get("MiddleName", None)),
                    Phone1=ValueField(value=employee_data.get("Contact", {}).get("Phone1", None)),
                    Phone1Type=ValueField(value=employee_data.get("Contact", {}).get("Phone1Type", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("Phone1Type"), dict) else employee_data.get("Contact", {}).get("Phone1Type")),
                    Phone2=ValueField(value=employee_data.get("Contact", {}).get("Phone2", None)),
                    Phone2Type=ValueField(value=employee_data.get("Contact", {}).get("Phone2Type", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("Phone2Type"), dict) else employee_data.get("Contact", {}).get("Phone2Type")),
                    Title=ValueField(value=employee_data.get("Contact", {}).get("Title", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("Title"), dict) else employee_data.get("Contact", {}).get("Title")),
                    Address=Address(
                        id=employee_data.get("Contact", {}).get("Address", {}).get("id", None),
                        rowNumber=employee_data.get("Contact", {}).get("Address", {}).get("rowNumber", None),
                        note=employee_data.get("Contact", {}).get("Address", {}).get("note", None),
                        AddressLine1=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("AddressLine1", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("Address", {}).get("AddressLine1"), dict) else employee_data.get("Contact", {}).get("Address", {}).get("AddressLine1")),
                        AddressLine2=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("AddressLine2", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("Address", {}).get("AddressLine2"), dict) else employee_data.get("Contact", {}).get("Address", {}).get("AddressLine2")),
                        City=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("City", None)),
                        Country=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("Country", {}).get("value", None) if isinstance(employee_data.get("Contact", {}).get("Address", {}).get("Country"), dict) else employee_data.get("Contact", {}).get("Address", {}).get("Country")),
                        PostalCode=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("PostalCode", None)),
                        State=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("State", None)),
                    )
                ),
                CurrencyID=ValueField(value=employee_data.get("CurrencyID", {}).get("value", None) if isinstance(employee_data.get("CurrencyID"), dict) else employee_data.get("CurrencyID")),
                DateOfBirth=ValueField(value=employee_data.get("DateOfBirth", {}).get("value", None) if isinstance(employee_data.get("DateOfBirth"), dict) else employee_data.get("DateOfBirth")),
                DepartmentID=ValueField(value=employee_data.get("DepartmentID", {}).get("value", None) if isinstance(employee_data.get("DepartmentID"), dict) else employee_data.get("DepartmentID")),
                EmployeeClassID=ValueField(value=employee_data.get("EmployeeClassID", {}).get("value", None) if isinstance(employee_data.get("EmployeeClassID"), dict) else employee_data.get("EmployeeClassID")),
                EmployeeID=ValueField(value=employee_data.get("EmployeeID", {}).get("value", None) if isinstance(employee_data.get("EmployeeID"), dict) else employee_data.get("EmployeeID")),
                EmploymentHistory=[
                    EmploymentHistory(
                        id=history.get("id"),
                        rowNumber=history.get("rowNumber"),
                        note=history.get("note"),
                        Active=ValueField(value=history.get("Active", {}).get("value", None) if isinstance(history.get("Active"), dict) else history.get("Active")),
                        EndDate=ValueField(value=history.get("EndDate")),
                        LineNbr=ValueField(value=history.get("LineNbr", {}).get("value", None) if isinstance(history.get("LineNbr"), dict) else history.get("LineNbr")),
                        PositionID=ValueField(value=history.get("PositionID", {}).get("value", None) if isinstance(history.get("PositionID"), dict) else history.get("PositionID")),
                        RehireEligible=ValueField(value=history.get("RehireEligible", {}).get("value", None) if isinstance(history.get("RehireEligible"), dict) else history.get("RehireEligible")),
                        StartDate=ValueField(value=history.get("StartDate", {}).get("value", None) if isinstance(history.get("StartDate"), dict) else history.get("StartDate")),
                        StartReason=ValueField(value=history.get("StartReason", {}).get("value", None) if isinstance(history.get("StartReason"), dict) else history.get("StartReason")),
                        Terminated=ValueField(value=history.get("Terminated", {}).get("value", None) if isinstance(history.get("Terminated"), dict) else history.get("Terminated")),
                        TerminationReason=ValueField(value=history.get("TerminationReason")),
                    ) for history in employee_data.get("EmploymentHistory", [])
                ],
                ExpenseAccount=ValueField(value=employee_data.get("ExpenseAccount", {}).get("value", None) if isinstance(employee_data.get("ExpenseAccount"), dict) else employee_data.get("ExpenseAccount")),
                ExpenseSubaccount=ValueField(value=employee_data.get("ExpenseSubaccount", {}).get("value", None) if isinstance(employee_data.get("ExpenseSubaccount"), dict) else employee_data.get("ExpenseSubaccount")),
                IdentityNumber=ValueField(value=employee_data.get("IdentityNumber", {}).get("value", None) if isinstance(employee_data.get("IdentityNumber"), dict) else employee_data.get("IdentityNumber")),
                IdentityType=ValueField(value=employee_data.get("IdentityType", {}).get("value", None) if isinstance(employee_data.get("IdentityType"), dict) else employee_data.get("IdentityType")),
                LastModifiedDateTime=ValueField(value=employee_data.get("LastModifiedDateTime")),
                Name=ValueField(value=employee_data.get("Name", {}).get("value", None) if isinstance(employee_data.get("Name"), dict) else employee_data.get("Name")),
                PaymentInstruction=[
                    PaymentInstruction(
                        id=payment.get("id"),
                        rowNumber=payment.get("rowNumber"),
                        note=payment.get("note"),
                        BAccountID=ValueField(value=payment.get("BAccountID", {}).get("value", None) if isinstance(payment.get("BAccountID"), dict) else payment.get("BAccountID")),
                        Description=ValueField(value=payment.get("Description", {}).get("value", None) if isinstance(payment.get("Description"), dict) else payment.get("Description")),
                        InstructionID=ValueField(value=payment.get("InstructionID", {}).get("value", None) if isinstance(payment.get("InstructionID"), dict) else payment.get("InstructionID")),
                        LocationID=ValueField(value=payment.get("LocationID", {}).get("value", None) if isinstance(payment.get("LocationID"), dict) else payment.get("LocationID")),
                        PaymentMethod=ValueField(value=payment.get("PaymentMethod", {}).get("value", None) if isinstance(payment.get("PaymentMethod"), dict) else payment.get("PaymentMethod")),
                        Value=ValueField(value=payment.get("Value", {}).get("value", None) if isinstance(payment.get("Value"), dict) else payment.get("Value)),
                    ) for payment in employee_data.get("PaymentInstruction", [])
                ],
                PaymentMethod=ValueField(value=employee_data.get("PaymentMethod", {}).get("value", None) if isinstance(employee_data.get("PaymentMethod"), dict) else employee_data.get("PaymentMethod")),
                ReportsToID=employee_data.get("ReportsToID"),
                SalesAccount=ValueField(value=employee_data.get("SalesAccount", {}).get("value", None) if isinstance(employee_data.get("SalesAccount"), dict) else employee_data.get("SalesAccount")),
                SalesSubaccount=ValueField(value=employee_data.get("SalesSubaccount", {}).get("value", None) if isinstance(employee_data.get("SalesSubaccount"), dict) else employee_data.get("SalesSubaccount")),
                Status=ValueField(value=employee_data.get("Status", {}).get("value", None) if isinstance(employee_data.get("Status"), dict) else employee_data.get("Status")),
                Custom=employee_data.get("Custom"),
                Links=employee_data.get("Links"),
            )
            return employee_response

        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
