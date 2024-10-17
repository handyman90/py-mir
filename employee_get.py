from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models import Employee, SessionLocal
from datetime import datetime

app = FastAPI()

# Token URL for authentication
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

# Pydantic model for the API response
from employee_get_models import EmployeeResponse

# Endpoint to retrieve employee information
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
            address = contact.get("Address", {})
            employment_history = employee_data.get("EmploymentHistory", [])
            payment_instruction = employee_data.get("PaymentInstruction", [])

            # Create or update employee record in the database
            existing_employee = db.query(Employee).filter(Employee.EmployeeID == employee_data.get("EmployeeID", {}).get("value")).first()

            if existing_employee:
                # Update existing employee
                existing_employee.row_number = employee_data.get("rowNumber")
                existing_employee.note = employee_data.get("note", "")
                existing_employee.BranchID = employee_data.get("BranchID", {}).get("value")
                existing_employee.Calendar = employee_data.get("Calendar", {}).get("value")
                existing_employee.CashAccount = employee_data.get("CashAccount", {}).get("value")
                existing_employee.ContactID = contact.get("id")
                existing_employee.ContactRowNumber = contact.get("rowNumber")
                existing_employee.ContactNote = contact.get("note")
                existing_employee.ContactDisplayName = contact.get("DisplayName", {}).get("value")
                existing_employee.ContactEmail = contact.get("Email", {}).get("value")
                existing_employee.ContactFax = contact.get("Fax", {}).get("value")
                existing_employee.ContactFirstName = contact.get("FirstName", {}).get("value")
                existing_employee.ContactLastName = contact.get("LastName", {}).get("value")
                existing_employee.ContactMiddleName = contact.get("MiddleName", {}).get("value")
                existing_employee.ContactPhone1 = contact.get("Phone1", {}).get("value")
                existing_employee.ContactPhone1Type = contact.get("Phone1Type", {}).get("value")
                existing_employee.ContactPhone2 = contact.get("Phone2", {}).get("value")
                existing_employee.ContactPhone2Type = contact.get("Phone2Type", {}).get("value")
                existing_employee.ContactTitle = contact.get("Title", {}).get("value")
                existing_employee.AddressID = address.get("id")
                existing_employee.AddressRowNumber = address.get("rowNumber")
                existing_employee.AddressNote = address.get("note")
                existing_employee.AddressLine1 = address.get("AddressLine1", {}).get("value")
                existing_employee.AddressLine2 = address.get("AddressLine2", {}).get("value")
                existing_employee.AddressCity = address.get("City", {}).get("value")
                existing_employee.AddressCountry = address.get("Country", {}).get("value")
                existing_employee.AddressPostalCode = address.get("PostalCode", {}).get("value")
                existing_employee.AddressState = address.get("State", {}).get("value")
                existing_employee.CurrencyID = employee_data.get("CurrencyID", {}).get("value")
                existing_employee.DateOfBirth = datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00"))
                existing_employee.DepartmentID = employee_data.get("DepartmentID", {}).get("value")
                existing_employee.EmployeeClassID = employee_data.get("EmployeeClassID", {}).get("value")
                existing_employee.EmployeeID = employee_data.get("EmployeeID", {}).get("value")
                existing_employee.EmploymentHistoryID = employment_history[0].get("id") if employment_history else None
                existing_employee.EmploymentHistoryRowNumber = employment_history[0].get("rowNumber") if employment_history else None
                existing_employee.EmploymentHistoryNote = employment_history[0].get("note") if employment_history else None
                existing_employee.EmploymentHistoryActive = employment_history[0].get("Active", {}).get("value") if employment_history else None
                existing_employee.EmploymentHistoryEndDate = employment_history[0].get("EndDate") if employment_history else None
                existing_employee.EmploymentHistoryLineNbr = employment_history[0].get("LineNbr", {}).get("value") if employment_history else None
                existing_employee.EmploymentHistoryPositionID = employment_history[0].get("PositionID", {}).get("value") if employment_history else None
                existing_employee.EmploymentHistoryRehireEligible = employment_history[0].get("RehireEligible", {}).get("value") if employment_history else None
                existing_employee.EmploymentHistoryStartDate = employment_history[0].get("StartDate", {}).get("value") if employment_history else None
                existing_employee.EmploymentHistoryStartReason = employment_history[0].get("StartReason", {}).get("value") if employment_history else None
                existing_employee.EmploymentHistoryTerminated = employment_history[0].get("Terminated", {}).get("value") if employment_history else None
                existing_employee.EmploymentHistoryTerminationReason = employment_history[0].get("TerminationReason", {}).get("value") if employment_history else None
                existing_employee.ExpenseAccount = employee_data.get("ExpenseAccount", {}).get("value")
                existing_employee.ExpenseSubaccount = employee_data.get("ExpenseSubaccount", {}).get("value")
                existing_employee.IdentityNumber = employee_data.get("IdentityNumber", {}).get("value")
                existing_employee.IdentityType = employee_data.get("IdentityType", {}).get("value")
                existing_employee.LastModifiedDateTime = datetime.fromisoformat(employee_data.get("LastModifiedDateTime", {}).get("value").replace("Z", "+00:00"))
                existing_employee.Name = employee_data.get("Name", {}).get("value")
                existing_employee.PaymentInstructionID = payment_instruction[0].get("id") if payment_instruction else None
                existing_employee.PaymentInstructionRowNumber = payment_instruction[0].get("rowNumber") if payment_instruction else None
                existing_employee.PaymentInstructionNote = payment_instruction[0].get("note") if payment_instruction else None
                existing_employee.PaymentInstructionBAccountID = payment_instruction[0].get("BAccountID", {}).get("value") if payment_instruction else None
                existing_employee.PaymentInstructionDescription = payment_instruction[0].get("Description", {}).get("value") if payment_instruction else None
                existing_employee.PaymentInstructionInstructionID = payment_instruction[0].get("InstructionID", {}).get("value") if payment_instruction else None
                existing_employee.PaymentInstructionLocationID = payment_instruction[0].get("LocationID", {}).get("value") if payment_instruction else None
                existing_employee.PaymentInstructionMethod = payment_instruction[0].get("PaymentMethod", {}).get("value") if payment_instruction else None
                existing_employee.PaymentInstructionValue = payment_instruction[0].get("Value", {}).get("value") if payment_instruction else None
                existing_employee.PaymentMethod = employee_data.get("PaymentMethod", {}).get("value")
                existing_employee.ReportsToID = employee_data.get("ReportsToID", {}).get("value")
                existing_employee.SalesAccount = employee_data.get("SalesAccount", {}).get("value")
                existing_employee.SalesSubaccount = employee_data.get("SalesSubaccount", {}).get("value")
                existing_employee.Status = employee_data.get("Status", {}).get("value")

            else:
                # Create a new employee record
                new_employee = Employee(
                    id=employee_data.get("EmployeeID", {}).get("value"),
                    row_number=employee_data.get("rowNumber"),
                    note=employee_data.get("note", ""),
                    BranchID=employee_data.get("BranchID", {}).get("value"),
                    Calendar=employee_data.get("Calendar", {}).get("value"),
                    CashAccount=employee_data.get("CashAccount", {}).get("value"),
                    ContactID=contact.get("id"),
                    ContactRowNumber=contact.get("rowNumber"),
                    ContactNote=contact.get("note"),
                    ContactDisplayName=contact.get("DisplayName", {}).get("value"),
                    ContactEmail=contact.get("Email", {}).get("value"),
                    ContactFax=contact.get("Fax", {}).get("value"),
                    ContactFirstName=contact.get("FirstName", {}).get("value"),
                    ContactLastName=contact.get("LastName", {}).get("value"),
                    ContactMiddleName=contact.get("MiddleName", {}).get("value"),
                    ContactPhone1=contact.get("Phone1", {}).get("value"),
                    ContactPhone1Type=contact.get("Phone1Type", {}).get("value"),
                    ContactPhone2=contact.get("Phone2", {}).get("value"),
                    ContactPhone2Type=contact.get("Phone2Type", {}).get("value"),
                    ContactTitle=contact.get("Title", {}).get("value"),
                    AddressID=address.get("id"),
                    AddressRowNumber=address.get("rowNumber"),
                    AddressNote=address.get("note"),
                    AddressLine1=address.get("AddressLine1", {}).get("value"),
                    AddressLine2=address.get("AddressLine2", {}).get("value"),
                    AddressCity=address.get("City", {}).get("value"),
                    AddressCountry=address.get("Country", {}).get("value"),
                    AddressPostalCode=address.get("PostalCode", {}).get("value"),
                    AddressState=address.get("State", {}).get("value"),
                    CurrencyID=employee_data.get("CurrencyID", {}).get("value"),
                    DateOfBirth=datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00")),
                    DepartmentID=employee_data.get("DepartmentID", {}).get("value"),
                    EmployeeClassID=employee_data.get("EmployeeClassID", {}).get("value"),
                    EmployeeID=employee_data.get("EmployeeID", {}).get("value"),
                    EmploymentHistoryID=employment_history[0].get("id") if employment_history else None,
                    EmploymentHistoryRowNumber=employment_history[0].get("rowNumber") if employment_history else None,
                    EmploymentHistoryNote=employment_history[0].get("note") if employment_history else None,
                    EmploymentHistoryActive=employment_history[0].get("Active", {}).get("value") if employment_history else None,
                    EmploymentHistoryEndDate=employment_history[0].get("EndDate") if employment_history else None,
                    EmploymentHistoryLineNbr=employment_history[0].get("LineNbr", {}).get("value") if employment_history else None,
                    EmploymentHistoryPositionID=employment_history[0].get("PositionID", {}).get("value") if employment_history else None,
                    EmploymentHistoryRehireEligible=employment_history[0].get("RehireEligible", {}).get("value") if employment_history else None,
                    EmploymentHistoryStartDate=employment_history[0].get("StartDate", {}).get("value") if employment_history else None,
                    EmploymentHistoryStartReason=employment_history[0].get("StartReason", {}).get("value") if employment_history else None,
                    EmploymentHistoryTerminated=employment_history[0].get("Terminated", {}).get("value") if employment_history else None,
                    EmploymentHistoryTerminationReason=employment_history[0].get("TerminationReason", {}).get("value") if employment_history else None,
                    ExpenseAccount=employee_data.get("ExpenseAccount", {}).get("value"),
                    ExpenseSubaccount=employee_data.get("ExpenseSubaccount", {}).get("value"),
                    IdentityNumber=employee_data.get("IdentityNumber", {}).get("value"),
                    IdentityType=employee_data.get("IdentityType", {}).get("value"),
                    LastModifiedDateTime=datetime.fromisoformat(employee_data.get("LastModifiedDateTime", {}).get("value").replace("Z", "+00:00")),
                    Name=employee_data.get("Name", {}).get("value"),
                    PaymentInstructionID=payment_instruction[0].get("id") if payment_instruction else None,
                    PaymentInstructionRowNumber=payment_instruction[0].get("rowNumber") if payment_instruction else None,
                    PaymentInstructionNote=payment_instruction[0].get("note") if payment_instruction else None,
                    PaymentInstructionBAccountID=payment_instruction[0].get("BAccountID", {}).get("value") if payment_instruction else None,
                    PaymentInstructionDescription=payment_instruction[0].get("Description", {}).get("value") if payment_instruction else None,
                    PaymentInstructionInstructionID=payment_instruction[0].get("InstructionID", {}).get("value") if payment_instruction else None,
                    PaymentInstructionLocationID=payment_instruction[0].get("LocationID", {}).get("value") if payment_instruction else None,
                    PaymentInstructionMethod=payment_instruction[0].get("PaymentMethod", {}).get("value") if payment_instruction else None,
                    PaymentInstructionValue=payment_instruction[0].get("Value", {}).get("value") if payment_instruction else None,
                    PaymentMethod=employee_data.get("PaymentMethod", {}).get("value"),
                    ReportsToID=employee_data.get("ReportsToID", {}).get("value"),
                    SalesAccount=employee_data.get("SalesAccount", {}).get("value"),
                    SalesSubaccount=employee_data.get("SalesSubaccount", {}).get("value"),
                    Status=employee_data.get("Status", {}).get("value")
                )
                db.add(new_employee)

            db.commit()
            return EmployeeResponse.from_orm(existing_employee if existing_employee else new_employee)

        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
