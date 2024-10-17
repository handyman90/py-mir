from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from models import Employee, SessionLocal
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
class Link(BaseModel):
    self: Optional[str]
    files_put: Optional[str]

class ValueField(BaseModel):
    value: Optional[str]

class Address(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    AddressLine1: ValueField
    AddressLine2: ValueField
    City: Optional[Dict]
    Country: ValueField
    PostalCode: Optional[Dict]
    State: Optional[Dict]
    custom: Optional[Dict]
    files: List[Dict]

class Contact(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Address: Address
    DisplayName: ValueField
    Email: ValueField
    Fax: Optional[Dict]
    FirstName: Optional[Dict]
    LastName: ValueField
    MiddleName: Optional[Dict]
    Phone1: Optional[Dict]
    Phone1Type: ValueField
    Phone2: Optional[Dict]
    Phone2Type: ValueField
    Title: ValueField
    WebSite: Optional[Dict]
    custom: Optional[Dict]
    files: List[Dict]

class EmploymentHistory(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    Active: ValueField
    EndDate: Optional[Dict]
    LineNbr: ValueField
    PositionID: ValueField
    RehireEligible: ValueField
    StartDate: ValueField
    StartReason: ValueField
    Terminated: ValueField
    TerminationReason: Optional[Dict]
    custom: Optional[Dict]
    files: List[Dict]

class PaymentInstruction(BaseModel):
    id: Optional[str]
    rowNumber: Optional[int]
    note: Optional[str]
    BAccountID: ValueField
    Description: ValueField
    InstructionID: ValueField
    LocationID: ValueField
    PaymentMethod: ValueField
    Value: ValueField
    custom: Optional[Dict]
    files: List[Dict]

class EmployeeResponse(BaseModel):
    id: str
    rowNumber: Optional[int] = None
    note: Optional[str] = None
    BranchID: ValueField
    Calendar: ValueField
    CashAccount: ValueField
    Contact: Contact
    CurrencyID: ValueField
    DateOfBirth: ValueField
    DepartmentID: ValueField
    EmployeeClassID: ValueField
    EmployeeID: ValueField
    EmploymentHistory: List[EmploymentHistory]
    ExpenseAccount: ValueField
    ExpenseSubaccount: ValueField
    IdentityNumber: ValueField
    IdentityType: ValueField
    LastModifiedDateTime: ValueField
    Name: ValueField
    PaymentInstruction: List[PaymentInstruction]
    ReportsToID: Optional[Dict]
    SalesAccount: ValueField
    SalesSubaccount: ValueField
    Status: ValueField
    custom: Optional[Dict]
    _links: Optional[Dict]
    files: List[Dict]

# Endpoint to retrieve and save employee information to database
@app.get("/organization/employee/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: str, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
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
            contact = employee_data.get("Contact", {})
            employee_history = employee_data.get("EmploymentHistory", [])
            payment_instructions = employee_data.get("PaymentInstruction", [])

            employee = Employee(
                id=employee_data.get("id"),
                row_number=employee_data.get("rowNumber"),
                note=employee_data.get("note"),
                BranchID=employee_data.get("BranchID", {}).get("value"),
                Calendar=employee_data.get("Calendar", {}).get("value"),
                CashAccount=employee_data.get("CashAccount", {}).get("value"),
                ContactID=contact.get("id"),
                ContactRowNumber=contact.get("rowNumber"),
                ContactNote=contact.get("note"),
                ContactDisplayName=contact.get("DisplayName", {}).get("value"),
                ContactEmail=contact.get("Email", {}).get("value"),
                ContactFax=contact.get("Fax"),
                ContactFirstName=contact.get("FirstName"),
                ContactLastName=contact.get("LastName", {}).get("value"),
                ContactMiddleName=contact.get("MiddleName"),
                ContactPhone1=contact.get("Phone1"),
                ContactPhone1Type=contact.get("Phone1Type", {}).get("value"),
                ContactPhone2=contact.get("Phone2"),
                ContactPhone2Type=contact.get("Phone2Type", {}).get("value"),
                ContactTitle=contact.get("Title", {}).get("value"),
                CurrencyID=employee_data.get("CurrencyID", {}).get("value"),
                DateOfBirth=datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00")),
                DepartmentID=employee_data.get("DepartmentID", {}).get("value"),
                EmployeeClassID=employee_data.get("EmployeeClassID", {}).get("value"),
                EmployeeID=employee_data.get("EmployeeID", {}).get("value"),
                EmploymentHistoryID=employee_history[0].get("id") if employee_history else None,
                EmploymentHistoryRowNumber=employee_history[0].get("rowNumber") if employee_history else None,
                EmploymentHistoryNote=employee_history[0].get("note") if employee_history else None,
                EmploymentHistoryActive=employee_history[0].get("Active", {}).get("value") if employee_history else None,
                EmploymentHistoryEndDate=employee_history[0].get("EndDate"),
                EmploymentHistoryLineNbr=employee_history[0].get("LineNbr", {}).get("value") if employee_history else None,
                EmploymentHistoryPositionID=employee_history[0].get("PositionID", {}).get("value") if employee_history else None,
                EmploymentHistoryRehireEligible=employee_history[0].get("RehireEligible", {}).get("value") if employee_history else None,
                EmploymentHistoryStartDate=employee_history[0].get("StartDate", {}).get("value") if employee_history else None,
                EmploymentHistoryStartReason=employee_history[0].get("StartReason", {}).get("value") if employee_history else None,
                EmploymentHistoryTerminated=employee_history[0].get("Terminated", {}).get("value") if employee_history else None,
                EmploymentHistoryTerminationReason=employee_history[0].get("TerminationReason"),
                ExpenseAccount=employee_data.get("ExpenseAccount", {}).get("value"),
                ExpenseSubaccount=employee_data.get("ExpenseSubaccount", {}).get("value"),
                IdentityNumber=employee_data.get("IdentityNumber", {}).get("value"),
                IdentityType=employee_data.get("IdentityType", {}).get("value"),
                LastModifiedDateTime=datetime.fromisoformat(employee_data.get("LastModifiedDateTime", {}).get("value").replace("Z", "+00:00")),
                Name=employee_data.get("Name", {}).get("value"),
                PaymentInstructionID=payment_instructions[0].get("id") if payment_instructions else None,
                PaymentInstructionRowNumber=payment_instructions[0].get("rowNumber") if payment_instructions else None,
                PaymentInstructionNote=payment_instructions[0].get("note") if payment_instructions else None,
                PaymentInstructionBAccountID=payment_instructions[0].get("BAccountID", {}).get("value") if payment_instructions else None,
                PaymentInstructionDescription=payment_instructions[0].get("Description", {}).get("value") if payment_instructions else None,
                PaymentInstructionInstructionID=payment_instructions[0].get("InstructionID", {}).get("value") if payment_instructions else None,
                PaymentInstructionLocationID=payment_instructions[0].get("LocationID", {}).get("value") if payment_instructions else None,
                PaymentInstructionMethod=payment_instructions[0].get("PaymentMethod", {}).get("value") if payment_instructions else None,
                PaymentInstructionValue=payment_instructions[0].get("Value", {}).get("value") if payment_instructions else None,
                PaymentMethod=employee_data.get("PaymentMethod", {}).get("value"),
                ReportsToID=employee_data.get("ReportsToID"),
                SalesAccount=employee_data.get("SalesAccount", {}).get("value"),
                SalesSubaccount=employee_data.get("SalesSubaccount", {}).get("value"),
                Status=employee_data.get("Status", {}).get("value"),
                Custom=employee_data.get("custom"),
                Links=employee_data.get("_links")
            )

            db.add(employee)
            db.commit()
            return employee  # return employee or relevant data here
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
