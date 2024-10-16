from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from sqlalchemy.orm import Session
from models import Employee, SessionLocal
from employee_get_models import EmployeeResponse, Contact, EmploymentHistory, PaymentInstruction
from datetime import datetime

app = FastAPI()

# Database connection string
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

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

# Endpoint to retrieve employee information
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
            employee_data = employee_data[0]  # Extract first record if it's a list

            # Create or update employee record in the database
            existing_employee = db.query(Employee).filter(Employee.id == employee_data["EmployeeID"]["value"]).first()

            if existing_employee:
                # Update existing employee fields
                existing_employee.row_number = employee_data.get("rowNumber")
                existing_employee.note = employee_data.get("note", "")
                existing_employee.BranchID = employee_data.get("BranchID", {}).get("value")
                existing_employee.Calendar = employee_data.get("Calendar", {}).get("value")
                existing_employee.CashAccount = employee_data.get("CashAccount", {}).get("value")
                existing_employee.ContactID = employee_data.get("Contact", {}).get("id")
                existing_employee.ContactRowNumber = employee_data.get("Contact", {}).get("rowNumber")
                existing_employee.ContactNote = employee_data.get("Contact", {}).get("note")
                existing_employee.ContactDisplayName = employee_data.get("Contact", {}).get("DisplayName", {}).get("value")
                existing_employee.ContactEmail = employee_data.get("Contact", {}).get("Email", {}).get("value")
                existing_employee.ContactFax = employee_data.get("Contact", {}).get("Fax")
                existing_employee.ContactFirstName = employee_data.get("Contact", {}).get("FirstName")
                existing_employee.ContactLastName = employee_data.get("Contact", {}).get("LastName", {}).get("value")
                existing_employee.ContactMiddleName = employee_data.get("Contact", {}).get("MiddleName")
                existing_employee.ContactPhone1 = employee_data.get("Contact", {}).get("Phone1")
                existing_employee.ContactPhone1Type = employee_data.get("Contact", {}).get("Phone1Type", {}).get("value")
                existing_employee.ContactPhone2 = employee_data.get("Contact", {}).get("Phone2")
                existing_employee.ContactPhone2Type = employee_data.get("Contact", {}).get("Phone2Type", {}).get("value")
                existing_employee.ContactTitle = employee_data.get("Contact", {}).get("Title", {}).get("value")
                existing_employee.AddressID = employee_data.get("Contact", {}).get("Address", {}).get("id")
                existing_employee.AddressRowNumber = employee_data.get("Contact", {}).get("Address", {}).get("rowNumber")
                existing_employee.AddressNote = employee_data.get("Contact", {}).get("Address", {}).get("note")
                existing_employee.AddressLine1 = employee_data.get("Contact", {}).get("Address", {}).get("AddressLine1", {}).get("value")
                existing_employee.AddressLine2 = employee_data.get("Contact", {}).get("Address", {}).get("AddressLine2", {}).get("value")
                existing_employee.AddressCity = employee_data.get("Contact", {}).get("Address", {}).get("City")
                existing_employee.AddressCountry = employee_data.get("Contact", {}).get("Address", {}).get("Country", {}).get("value")
                existing_employee.AddressPostalCode = employee_data.get("Contact", {}).get("Address", {}).get("PostalCode")
                existing_employee.AddressState = employee_data.get("Contact", {}).get("Address", {}).get("State")

                existing_employee.CurrencyID = employee_data.get("CurrencyID", {}).get("value")
                existing_employee.DateOfBirth = datetime.fromisoformat(employee_data.get("DateOfBirth", {}).get("value").replace("Z", "+00:00"))
                existing_employee.DepartmentID = employee_data.get("DepartmentID", {}).get("value")
                existing_employee.EmployeeClassID = employee_data.get("EmployeeClassID", {}).get("value")
                existing_employee.EmployeeID = employee_data.get("EmployeeID", {}).get("value")
                existing_employee.EmploymentHistoryID = employee_data.get("EmploymentHistory", [{}])[0].get("id")
                existing_employee.EmploymentHistoryRowNumber = employee_data.get("EmploymentHistory", [{}])[0].get("rowNumber")
                existing_employee.EmploymentHistoryNote = employee_data.get("EmploymentHistory", [{}])[0].get("note")
                existing_employee.EmploymentHistoryActive = employee_data.get("EmploymentHistory", [{}])[0].get("Active", {}).get("value")
                existing_employee.EmploymentHistoryEndDate = employee_data.get("EmploymentHistory", [{}])[0].get("EndDate")
                existing_employee.EmploymentHistoryLineNbr = employee_data.get("EmploymentHistory", [{}])[0].get("LineNbr", {}).get("value")
                existing_employee.EmploymentHistoryPositionID = employee_data.get("EmploymentHistory", [{}])[0].get("PositionID", {}).get("value")
                existing_employee.EmploymentHistoryRehireEligible = employee_data.get("EmploymentHistory", [{}])[0].get("RehireEligible", {}).get("value")
                existing_employee.EmploymentHistoryStartDate = employee_data.get("EmploymentHistory", [{}])[0].get("StartDate", {}).get("value")
                existing_employee.EmploymentHistoryStartReason = employee_data.get("EmploymentHistory", [{}])[0].get("StartReason", {}).get("value")
                existing_employee.EmploymentHistoryTerminated = employee_data.get("EmploymentHistory", [{}])[0].get("Terminated", {}).get("value")
                existing_employee.EmploymentHistoryTerminationReason = employee_data.get("EmploymentHistory", [{}])[0].get("TerminationReason")

                existing_employee.ExpenseAccount = employee_data.get("ExpenseAccount", {}).get("value")
                existing_employee.ExpenseSubaccount = employee_data.get("ExpenseSubaccount", {}).get("value")
                existing_employee.IdentityNumber = employee_data.get("IdentityNumber", {}).get("value")
                existing_employee.IdentityType = employee_data.get("IdentityType", {}).get("value")
                existing_employee.LastModifiedDateTime = datetime.fromisoformat(employee_data.get("LastModifiedDateTime", {}).get("value").replace("Z", "+00:00"))
                existing_employee.Name = employee_data.get("Name", {}).get("value")
                existing_employee.PaymentInstructionID = employee_data.get("PaymentInstruction", [{}])[0].get("id")
                existing_employee.PaymentInstructionRowNumber = employee_data.get("PaymentInstruction", [{}])[0].get("rowNumber")
                existing_employee.PaymentInstructionNote = employee_data.get("PaymentInstruction", [{}])[0].get("note")
                existing_employee.PaymentInstructionBAccountID = employee_data.get("PaymentInstruction", [{}])[0].get("BAccountID", {}).get("value")
                existing_employee.PaymentInstructionDescription = employee_data.get("PaymentInstruction", [{}])[0].get("Description", {}).get("value")
                existing_employee.PaymentInstructionInstructionID = employee_data.get("PaymentInstruction", [{}])[0].get("InstructionID", {}).get("value")
                existing_employee.PaymentInstructionLocationID = employee_data.get("PaymentInstruction", [{}])[0].get("LocationID", {}).get("value")
                existing_employee.PaymentInstructionMethod = employee_data.get("PaymentInstruction", [{}])[0].get("PaymentMethod", {}).get("value")
                existing_employee.PaymentInstructionValue = employee_data.get("PaymentInstruction", [{}])[0].get("Value", {}).get("value")

                existing_employee.PaymentMethod = employee_data.get("PaymentMethod", {}).get("value")
                existing_employee.ReportsToID = employee_data.get("ReportsToID", {}).get("value")
                existing_employee.SalesAccount = employee_data.get("SalesAccount", {}).get("value")
                existing_employee.SalesSubaccount = employee_data.get("SalesSubaccount", {}).get("value")
                existing_employee.Status = employee_data.get("Status", {}).get("value")
                existing_employee.Custom = employee_data.get("custom", {})
                existing_employee.Links = employee_data.get("_links", {})

            else:
                # Create a new employee record
                employee = Employee(
                    id=employee_data.get("EmployeeID", {}).get("value"),
                    row_number=employee_data.get("rowNumber"),
                    note=employee_data.get("note", ""),
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
                    EmploymentHistoryID=employee_data.get("EmploymentHistory", [{}])[0].get("id"),
                    EmploymentHistoryRowNumber=employee_data.get("EmploymentHistory", [{}])[0].get("rowNumber"),
                    EmploymentHistoryNote=employee_data.get("EmploymentHistory", [{}])[0].get("note"),
                    EmploymentHistoryActive=employee_data.get("EmploymentHistory", [{}])[0].get("Active", {}).get("value"),
                    EmploymentHistoryEndDate=employee_data.get("EmploymentHistory", [{}])[0].get("EndDate"),
                    EmploymentHistoryLineNbr=employee_data.get("EmploymentHistory", [{}])[0].get("LineNbr", {}).get("value"),
                    EmploymentHistoryPositionID=employee_data.get("EmploymentHistory", [{}])[0].get("PositionID", {}).get("value"),
                    EmploymentHistoryRehireEligible=employee_data.get("EmploymentHistory", [{}])[0].get("RehireEligible", {}).get("value"),
                    EmploymentHistoryStartDate=employee_data.get("EmploymentHistory", [{}])[0].get("StartDate", {}).get("value"),
                    EmploymentHistoryStartReason=employee_data.get("EmploymentHistory", [{}])[0].get("StartReason", {}).get("value"),
                    EmploymentHistoryTerminated=employee_data.get("EmploymentHistory", [{}])[0].get("Terminated", {}).get("value"),
                    EmploymentHistoryTerminationReason=employee_data.get("EmploymentHistory", [{}])[0].get("TerminationReason"),
                    ExpenseAccount=employee_data.get("ExpenseAccount", {}).get("value"),
                    ExpenseSubaccount=employee_data.get("ExpenseSubaccount", {}).get("value"),
                    IdentityNumber=employee_data.get("IdentityNumber", {}).get("value"),
                    IdentityType=employee_data.get("IdentityType", {}).get("value"),
                    LastModifiedDateTime=datetime.fromisoformat(employee_data.get("LastModifiedDateTime", {}).get("value").replace("Z", "+00:00")),
                    Name=employee_data.get("Name", {}).get("value"),
                    PaymentInstructionID=employee_data.get("PaymentInstruction", [{}])[0].get("id"),
                    PaymentInstructionRowNumber=employee_data.get("PaymentInstruction", [{}])[0].get("rowNumber"),
                    PaymentInstructionNote=employee_data.get("PaymentInstruction", [{}])[0].get("note"),
                    PaymentInstructionBAccountID=employee_data.get("PaymentInstruction", [{}])[0].get("BAccountID", {}).get("value"),
                    PaymentInstructionDescription=employee_data.get("PaymentInstruction", [{}])[0].get("Description", {}).get("value"),
                    PaymentInstructionInstructionID=employee_data.get("PaymentInstruction", [{}])[0].get("InstructionID", {}).get("value"),
                    PaymentInstructionLocationID=employee_data.get("PaymentInstruction", [{}])[0].get("LocationID", {}).get("value"),
                    PaymentInstructionMethod=employee_data.get("PaymentInstruction", [{}])[0].get("PaymentMethod", {}).get("value"),
                    PaymentInstructionValue=employee_data.get("PaymentInstruction", [{}])[0].get("Value", {}).get("value"),
                    PaymentMethod=employee_data.get("PaymentMethod", {}).get("value"),
                    ReportsToID=employee_data.get("ReportsToID", {}).get("value"),
                    SalesAccount=employee_data.get("SalesAccount", {}).get("value"),
                    SalesSubaccount=employee_data.get("SalesSubaccount", {}).get("value"),
                    Status=employee_data.get("Status", {}).get("value"),
                    Custom=employee_data.get("custom", {}),
                    Links=employee_data.get("_links", {})
                )
                db.add(employee)

            db.commit()
            return EmployeeResponse(
                id=existing_employee.id if existing_employee else employee.id,
                rowNumber=existing_employee.row_number if existing_employee else employee.row_number,
                note=existing_employee.note if existing_employee else employee.note,
                BranchID={"value": existing_employee.BranchID} if existing_employee else {"value": employee.BranchID},
                Calendar={"value": existing_employee.Calendar} if existing_employee else {"value": employee.Calendar},
                CashAccount={"value": existing_employee.CashAccount} if existing_employee else {"value": employee.CashAccount},
                Contact=Contact(
                    id=existing_employee.ContactID if existing_employee else employee.ContactID,
                    rowNumber=existing_employee.ContactRowNumber if existing_employee else employee.ContactRowNumber,
                    note=existing_employee.ContactNote if existing_employee else employee.ContactNote,
                    DisplayName={"value": existing_employee.ContactDisplayName} if existing_employee else {"value": employee.ContactDisplayName},
                    Email={"value": existing_employee.ContactEmail} if existing_employee else {"value": employee.ContactEmail},
                    Fax={"value": existing_employee.ContactFax} if existing_employee else {"value": employee.ContactFax},
                    FirstName={"value": existing_employee.ContactFirstName} if existing_employee else {"value": employee.ContactFirstName},
                    LastName={"value": existing_employee.ContactLastName} if existing_employee else {"value": employee.ContactLastName},
                    MiddleName={"value": existing_employee.ContactMiddleName} if existing_employee else {"value": employee.ContactMiddleName},
                    Phone1={"value": existing_employee.ContactPhone1} if existing_employee else {"value": employee.ContactPhone1},
                    Phone1Type={"value": existing_employee.ContactPhone1Type} if existing_employee else {"value": employee.ContactPhone1Type},
                    Phone2={"value": existing_employee.ContactPhone2} if existing_employee else {"value": employee.ContactPhone2},
                    Phone2Type={"value": existing_employee.ContactPhone2Type} if existing_employee else {"value": employee.ContactPhone2Type},
                    Title={"value": existing_employee.ContactTitle} if existing_employee else {"value": employee.ContactTitle},
                    Address=Address(
                        id=existing_employee.AddressID if existing_employee else employee.AddressID,
                        rowNumber=existing_employee.AddressRowNumber if existing_employee else employee.AddressRowNumber,
                        note=existing_employee.AddressNote if existing_employee else employee.AddressNote,
                        AddressLine1={"value": existing_employee.AddressLine1} if existing_employee else {"value": employee.AddressLine1},
                        AddressLine2={"value": existing_employee.AddressLine2} if existing_employee else {"value": employee.AddressLine2},
                        City={"value": existing_employee.AddressCity} if existing_employee else {"value": employee.AddressCity},
                        Country={"value": existing_employee.AddressCountry} if existing_employee else {"value": employee.AddressCountry},
                        PostalCode={"value": existing_employee.AddressPostalCode} if existing_employee else {"value": employee.AddressPostalCode},
                        State={"value": existing_employee.AddressState} if existing_employee else {"value": employee.AddressState},
                    ),
                ),
                CurrencyID={"value": existing_employee.CurrencyID} if existing_employee else {"value": employee.CurrencyID},
                DateOfBirth={"value": existing_employee.DateOfBirth.isoformat()} if existing_employee else {"value": employee.DateOfBirth.isoformat()},
                DepartmentID={"value": existing_employee.DepartmentID} if existing_employee else {"value": employee.DepartmentID},
                EmployeeClassID={"value": existing_employee.EmployeeClassID} if existing_employee else {"value": employee.EmployeeClassID},
                EmployeeID={"value": existing_employee.EmployeeID} if existing_employee else {"value": employee.EmployeeID},
                EmploymentHistory=[
                    EmploymentHistory(
                        id=existing_employee.EmploymentHistoryID if existing_employee else employee.EmploymentHistoryID,
                        rowNumber=existing_employee.EmploymentHistoryRowNumber if existing_employee else employee.EmploymentHistoryRowNumber,
                        note=existing_employee.EmploymentHistoryNote if existing_employee else employee.EmploymentHistoryNote,
                        Active={"value": existing_employee.EmploymentHistoryActive} if existing_employee else {"value": employee.EmploymentHistoryActive},
                        EndDate={"value": existing_employee.EmploymentHistoryEndDate.isoformat()} if existing_employee and existing_employee.EmploymentHistoryEndDate else None,
                        LineNbr={"value": existing_employee.EmploymentHistoryLineNbr} if existing_employee else {"value": employee.EmploymentHistoryLineNbr},
                        PositionID={"value": existing_employee.EmploymentHistoryPositionID} if existing_employee else {"value": employee.EmploymentHistoryPositionID},
                        RehireEligible={"value": existing_employee.EmploymentHistoryRehireEligible} if existing_employee else {"value": employee.EmploymentHistoryRehireEligible},
                        StartDate={"value": existing_employee.EmploymentHistoryStartDate.isoformat()} if existing_employee else {"value": employee.EmploymentHistoryStartDate.isoformat()},
                        StartReason={"value": existing_employee.EmploymentHistoryStartReason} if existing_employee else {"value": employee.EmploymentHistoryStartReason},
                        Terminated={"value": existing_employee.EmploymentHistoryTerminated} if existing_employee else {"value": employee.EmploymentHistoryTerminated},
                        TerminationReason={"value": existing_employee.EmploymentHistoryTerminationReason} if existing_employee else {"value": employee.EmploymentHistoryTerminationReason},
                    ) for _ in range(1)  # Creating a single EmploymentHistory object
                ],
                ExpenseAccount={"value": existing_employee.ExpenseAccount} if existing_employee else {"value": employee.ExpenseAccount},
                ExpenseSubaccount={"value": existing_employee.ExpenseSubaccount} if existing_employee else {"value": employee.ExpenseSubaccount},
                IdentityNumber={"value": existing_employee.IdentityNumber} if existing_employee else {"value": employee.IdentityNumber},
                IdentityType={"value": existing_employee.IdentityType} if existing_employee else {"value": employee.IdentityType},
                LastModifiedDateTime={"value": existing_employee.LastModifiedDateTime.isoformat()} if existing_employee else {"value": employee.LastModifiedDateTime.isoformat()},
                Name={"value": existing_employee.Name} if existing_employee else {"value": employee.Name},
                PaymentInstruction=[
                    PaymentInstruction(
                        id=existing_employee.PaymentInstructionID if existing_employee else employee.PaymentInstructionID,
                        rowNumber=existing_employee.PaymentInstructionRowNumber if existing_employee else employee.PaymentInstructionRowNumber,
                        note=existing_employee.PaymentInstructionNote if existing_employee else employee.PaymentInstructionNote,
                        BAccountID={"value": existing_employee.PaymentInstructionBAccountID} if existing_employee else {"value": employee.PaymentInstructionBAccountID},
                        Description={"value": existing_employee.PaymentInstructionDescription} if existing_employee else {"value": employee.PaymentInstructionDescription},
                        InstructionID={"value": existing_employee.PaymentInstructionInstructionID} if existing_employee else {"value": employee.PaymentInstructionInstructionID},
                        LocationID={"value": existing_employee.PaymentInstructionLocationID} if existing_employee else {"value": employee.PaymentInstructionLocationID},
                        PaymentMethod={"value": existing_employee.PaymentInstructionMethod} if existing_employee else {"value": employee.PaymentInstructionMethod},
                        Value={"value": existing_employee.PaymentInstructionValue} if existing_employee else {"value": employee.PaymentInstructionValue},
                    ) for _ in range(1)  # Creating a single PaymentInstruction object
                ],
                PaymentMethod={"value": existing_employee.PaymentMethod} if existing_employee else {"value": employee.PaymentMethod},
                ReportsToID={"value": existing_employee.ReportsToID} if existing_employee else {"value": employee.ReportsToID},
                SalesAccount={"value": existing_employee.SalesAccount} if existing_employee else {"value": employee.SalesAccount},
                SalesSubaccount={"value": existing_employee.SalesSubaccount} if existing_employee else {"value": employee.SalesSubaccount},
                Status={"value": existing_employee.Status} if existing_employee else {"value": employee.Status},
                Custom=existing_employee.Custom if existing_employee else employee.Custom,
                Links=existing_employee.Links if existing_employee else employee.Links,
            )

        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
