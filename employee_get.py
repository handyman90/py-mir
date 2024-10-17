from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from models import SessionLocal, Employee
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
    value: Optional[str]

class EmployeeResponse(BaseModel):
    id: str
    rowNumber: Optional[int]
    note: Optional[str]
    BranchID: ValueField
    Calendar: ValueField
    CashAccount: ValueField
    Contact: Dict[str, Any]
    CurrencyID: ValueField
    DateOfBirth: ValueField
    DepartmentID: ValueField
    EmployeeClassID: ValueField
    EmployeeID: ValueField
    EmploymentHistory: List[Dict[str, Any]]
    ExpenseAccount: ValueField
    ExpenseSubaccount: ValueField
    IdentityNumber: ValueField
    IdentityType: ValueField
    LastModifiedDateTime: Optional[str]
    Name: ValueField
    PaymentInstruction: List[Dict[str, Any]]
    PaymentMethod: ValueField
    ReportsToID: Optional[Dict[str, Any]]
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    Custom: Optional[Dict[str, Any]]
    Links: Optional[Dict[str, Any]]

# Endpoint to retrieve and save employee information to database
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
            
            # Flatten nested fields and create a new employee object or update an existing one
            employee = Employee(
                id=employee_data.get("id"),
                row_number=employee_data.get("rowNumber"),
                note=employee_data.get("note"),
                BranchID=employee_data.get("BranchID", {}).get("value"),
                Calendar=employee_data.get("Calendar", {}).get("value"),
                CashAccount=employee_data.get("CashAccount", {}).get("value"),
                ContactID=employee_data.get("Contact", {}).get("id"),
                ContactRowNumber=employee_data.get("Contact", {}).get("rowNumber"),
                ContactNote=employee_data.get("Contact", {}).get("note"),
                ContactDisplayName=employee_data.get("Contact", {}).get("DisplayName", {}).get("value"),
                ContactEmail=employee_data.get("Contact", {}).get("Email", {}).get("value"),
                ContactFax=employee_data.get("Contact", {}).get("Fax"),
                ContactFirstName=employee_data.get("Contact", {}).get("FirstName"),
                ContactLastName=employee_data.get("Contact", {}).get("LastName", {}).get("value"),
                ContactMiddleName=employee_data.get("Contact", {}).get("MiddleName"),
                ContactPhone1=employee_data.get("Contact", {}).get("Phone1"),
                ContactPhone1Type=employee_data.get("Contact", {}).get("Phone1Type", {}).get("value"),
                ContactPhone2=employee_data.get("Contact", {}).get("Phone2"),
                ContactPhone2Type=employee_data.get("Contact", {}).get("Phone2Type", {}).get("value"),
                ContactTitle=employee_data.get("Contact", {}).get("Title", {}).get("value"),
                AddressID=employee_data.get("Contact", {}).get("Address", {}).get("id"),
                AddressRowNumber=employee_data.get("Contact", {}).get("Address", {}).get("rowNumber"),
                AddressNote=employee_data.get("Contact", {}).get("Address", {}).get("note"),
                AddressLine1=employee_data.get("Contact", {}).get("Address", {}).get("AddressLine1", {}).get("value"),
                AddressLine2=employee_data.get("Contact", {}).get("Address", {}).get("AddressLine2", {}).get("value"),
                AddressCity=employee_data.get("Contact", {}).get("Address", {}).get("City"),
                AddressCountry=employee_data.get("Contact", {}).get("Address", {}).get("Country", {}).get("value"),
                AddressPostalCode=employee_data.get("Contact", {}).get("Address", {}).get("PostalCode"),
                AddressState=employee_data.get("Contact", {}).get("Address", {}).get("State"),
                CurrencyID=employee_data.get("CurrencyID", {}).get("value"),
                DateOfBirth=datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00")),
                DepartmentID=employee_data.get("DepartmentID", {}).get("value"),
                EmployeeClassID=employee_data.get("EmployeeClassID", {}).get("value"),
                EmployeeID=employee_data.get("EmployeeID", {}).get("value"),
                EmploymentHistoryID=employee_data.get("EmploymentHistory", [])[0].get("id") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryRowNumber=employee_data.get("EmploymentHistory", [])[0].get("rowNumber") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryNote=employee_data.get("EmploymentHistory", [])[0].get("note") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryActive=employee_data.get("EmploymentHistory", [])[0].get("Active", {}).get("value") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryEndDate=employee_data.get("EmploymentHistory", [])[0].get("EndDate"),
                EmploymentHistoryLineNbr=employee_data.get("EmploymentHistory", [])[0].get("LineNbr", {}).get("value") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryPositionID=employee_data.get("EmploymentHistory", [])[0].get("PositionID", {}).get("value") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryRehireEligible=employee_data.get("EmploymentHistory", [])[0].get("RehireEligible", {}).get("value") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryStartDate=employee_data.get("EmploymentHistory", [])[0].get("StartDate", {}).get("value") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryStartReason=employee_data.get("EmploymentHistory", [])[0].get("StartReason", {}).get("value") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryTerminated=employee_data.get("EmploymentHistory", [])[0].get("Terminated", {}).get("value") if employee_data.get("EmploymentHistory") else None,
                EmploymentHistoryTerminationReason=employee_data.get("EmploymentHistory", [])[0].get("TerminationReason", {}).get("value") if employee_data.get("EmploymentHistory") else None,
                ExpenseAccount=employee_data.get("ExpenseAccount", {}).get("value"),
                ExpenseSubaccount=employee_data.get("ExpenseSubaccount", {}).get("value"),
                IdentityNumber=employee_data.get("IdentityNumber", {}).get("value"),
                IdentityType=employee_data.get("IdentityType", {}).get("value"),
                LastModifiedDateTime=datetime.fromisoformat(employee_data.get("LastModifiedDateTime", {}).get("value").replace("Z", "+00:00")),
                Name=employee_data.get("Name", {}).get("value"),
                PaymentInstructionID=employee_data.get("PaymentInstruction", [])[0].get("id") if employee_data.get("PaymentInstruction") else None,
                PaymentInstructionRowNumber=employee_data.get("PaymentInstruction", [])[0].get("rowNumber") if employee_data.get("PaymentInstruction") else None,
                PaymentInstructionNote=employee_data.get("PaymentInstruction", [])[0].get("note") if employee_data.get("PaymentInstruction") else None,
                PaymentInstructionBAccountID=employee_data.get("PaymentInstruction", [])[0].get("BAccountID", {}).get("value") if employee_data.get("PaymentInstruction") else None,
                PaymentInstructionDescription=employee_data.get("PaymentInstruction", [])[0].get("Description", {}).get("value") if employee_data.get("PaymentInstruction") else None,
                PaymentInstructionInstructionID=employee_data.get("PaymentInstruction", [])[0].get("InstructionID", {}).get("value") if employee_data.get("PaymentInstruction") else None,
                PaymentInstructionLocationID=employee_data.get("PaymentInstruction", [])[0].get("LocationID", {}).get("value") if employee_data.get("PaymentInstruction") else None,
                PaymentInstructionMethod=employee_data.get("PaymentInstruction", [])[0].get("PaymentMethod", {}).get("value") if employee_data.get("PaymentInstruction") else None,
                PaymentInstructionValue=employee_data.get("PaymentInstruction", [])[0].get("Value", {}).get("value") if employee_data.get("PaymentInstruction") else None,
                PaymentMethod=employee_data.get("PaymentMethod", {}).get("value"),
                ReportsToID=employee_data.get("ReportsToID", {}).get("value"),
                SalesAccount=employee_data.get("SalesAccount", {}).get("value"),
                SalesSubaccount=employee_data.get("SalesSubaccount", {}).get("value"),
                Status=employee_data.get("Status", {}).get("value"),
                Custom=employee_data.get("Custom"),
                Links=employee_data.get("Links")
            )
            
            # Add or update the employee in the database
            db.add(employee)
            db.commit()

            return employee

        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
