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
                BranchID=ValueField(value=employee_data.get("BranchID", {}).get("value")),
                Calendar=ValueField(value=employee_data.get("Calendar", {}).get("value")),
                CashAccount=ValueField(value=employee_data.get("CashAccount", {}).get("value")),
                Contact=Contact(
                    id=employee_data.get("Contact", {}).get("id"),
                    rowNumber=employee_data.get("Contact", {}).get("rowNumber"),
                    note=employee_data.get("Contact", {}).get("note"),
                    DisplayName=ValueField(value=employee_data.get("Contact", {}).get("DisplayName", {}).get("value")),
                    Email=ValueField(value=employee_data.get("Contact", {}).get("Email", {}).get("value")),
                    Fax=ValueField(value=employee_data.get("Contact", {}).get("Fax")),
                    FirstName=ValueField(value=employee_data.get("Contact", {}).get("FirstName", {}).get("value")),
                    LastName=ValueField(value=employee_data.get("Contact", {}).get("LastName", {}).get("value")),
                    MiddleName=ValueField(value=employee_data.get("Contact", {}).get("MiddleName")),
                    Phone1=ValueField(value=employee_data.get("Contact", {}).get("Phone1")),
                    Phone1Type=ValueField(value=employee_data.get("Contact", {}).get("Phone1Type", {}).get("value")),
                    Phone2=ValueField(value=employee_data.get("Contact", {}).get("Phone2")),
                    Phone2Type=ValueField(value=employee_data.get("Contact", {}).get("Phone2Type", {}).get("value")),
                    Title=ValueField(value=employee_data.get("Contact", {}).get("Title", {}).get("value")),
                    Address=Address(
                        id=employee_data.get("Contact", {}).get("Address", {}).get("id"),
                        rowNumber=employee_data.get("Contact", {}).get("Address", {}).get("rowNumber"),
                        note=employee_data.get("Contact", {}).get("Address", {}).get("note"),
                        AddressLine1=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("AddressLine1", {}).get("value")),
                        AddressLine2=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("AddressLine2", {}).get("value")),
                        City=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("City")),
                        Country=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("Country", {}).get("value")),
                        PostalCode=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("PostalCode")),
                        State=ValueField(value=employee_data.get("Contact", {}).get("Address", {}).get("State")),
                    )
                ),
                CurrencyID=ValueField(value=employee_data.get("CurrencyID", {}).get("value")),
                DateOfBirth=ValueField(value=employee_data.get("DateOfBirth", {}).get("value")),
                DepartmentID=ValueField(value=employee_data.get("DepartmentID", {}).get("value")),
                EmployeeClassID=ValueField(value=employee_data.get("EmployeeClassID", {}).get("value")),
                EmployeeID=ValueField(value=employee_data.get("EmployeeID", {}).get("value")),
                EmploymentHistory=[
                    EmploymentHistory(
                        id=history.get("id"),
                        rowNumber=history.get("rowNumber"),
                        note=history.get("note"),
                        Active=ValueField(value=history.get("Active", {}).get("value")),
                        EndDate=ValueField(value=history.get("EndDate")),
                        LineNbr=ValueField(value=history.get("LineNbr", {}).get("value")),
                        PositionID=ValueField(value=history.get("PositionID", {}).get("value")),
                        RehireEligible=ValueField(value=history.get("RehireEligible", {}).get("value")),
                        StartDate=ValueField(value=history.get("StartDate", {}).get("value")),
                        StartReason=ValueField(value=history.get("StartReason", {}).get("value")),
                        Terminated=ValueField(value=history.get("Terminated", {}).get("value")),
                        TerminationReason=ValueField(value=history.get("TerminationReason")),
                    ) for history in employee_data.get("EmploymentHistory", [])
                ],
                ExpenseAccount=ValueField(value=employee_data.get("ExpenseAccount", {}).get("value")),
                ExpenseSubaccount=ValueField(value=employee_data.get("ExpenseSubaccount", {}).get("value")),
                IdentityNumber=ValueField(value=employee_data.get("IdentityNumber", {}).get("value")),
                IdentityType=ValueField(value=employee_data.get("IdentityType", {}).get("value")),
                LastModifiedDateTime=ValueField(value=employee_data.get("LastModifiedDateTime")),
                Name=ValueField(value=employee_data.get("Name", {}).get("value")),
                PaymentInstruction=[
                    PaymentInstruction(
                        id=payment.get("id"),
                        rowNumber=payment.get("rowNumber"),
                        note=payment.get("note"),
                        BAccountID=ValueField(value=payment.get("BAccountID", {}).get("value")),
                        Description=ValueField(value=payment.get("Description", {}).get("value")),
                        InstructionID=ValueField(value=payment.get("InstructionID", {}).get("value")),
                        LocationID=ValueField(value=payment.get("LocationID", {}).get("value")),
                        PaymentMethod=ValueField(value=payment.get("PaymentMethod", {}).get("value")),
                        Value=ValueField(value=payment.get("Value", {}).get("value")),
                    ) for payment in employee_data.get("PaymentInstruction", [])
                ],
                PaymentMethod=ValueField(value=employee_data.get("PaymentMethod", {}).get("value")),
                ReportsToID=employee_data.get("ReportsToID"),
                SalesAccount=ValueField(value=employee_data.get("SalesAccount", {}).get("value")),
                SalesSubaccount=ValueField(value=employee_data.get("SalesSubaccount", {}).get("value")),
                Status=ValueField(value=employee_data.get("Status", {}).get("value")),
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
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Changed to 0.0.0.0 to accept requests from any IP
