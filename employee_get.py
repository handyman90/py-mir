from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from sqlalchemy.orm import Session
from models import Employee, Contact, Address, EmploymentHistory, PaymentInstruction, SessionLocal
from employee_get_models import EmployeeResponse
from datetime import datetime

app = FastAPI()

# Token URL and payload for authentication
token_url = "https://csmstg.censof.com/2023R1Preprod/identity/connect/token"

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

# Function to save employee data to the database
def save_employee_to_db(db: Session, employee_data: EmployeeResponse):
    # Check if the employee already exists
    existing_employee = db.query(Employee).filter(Employee.employee_id == employee_data.EmployeeID.value).first()

    if existing_employee:
        # Update existing employee record
        existing_employee.branch_id = employee_data.BranchID.value
        existing_employee.calendar = employee_data.Calendar.value
        existing_employee.cash_account = employee_data.CashAccount.value
        existing_employee.currency_id = employee_data.CurrencyID.value
        existing_employee.date_of_birth = datetime.fromisoformat(employee_data.DateOfBirth.value)
        existing_employee.department_id = employee_data.DepartmentID.value
        existing_employee.employee_class_id = employee_data.EmployeeClassID.value
        existing_employee.name = employee_data.Name.value
        existing_employee.payment_method = employee_data.PaymentMethod.value
        existing_employee.status = employee_data.Status.value
        existing_employee.expense_account = employee_data.ExpenseAccount.value
        existing_employee.expense_subaccount = employee_data.ExpenseSubaccount.value
        existing_employee.identity_number = employee_data.IdentityNumber.value
        existing_employee.identity_type = employee_data.IdentityType.value
        existing_employee.last_modified_date_time = datetime.fromisoformat(employee_data.LastModifiedDateTime.value)

        db.commit()
    else:
        # Create a new employee record
        new_employee = Employee(
            id=employee_data.id,
            row_number=employee_data.rowNumber,
            branch_id=employee_data.BranchID.value,
            calendar=employee_data.Calendar.value,
            cash_account=employee_data.CashAccount.value,
            currency_id=employee_data.CurrencyID.value,
            date_of_birth=datetime.fromisoformat(employee_data.DateOfBirth.value),
            department_id=employee_data.DepartmentID.value,
            employee_class_id=employee_data.EmployeeClassID.value,
            employee_id=employee_data.EmployeeID.value,
            name=employee_data.Name.value,
            payment_method=employee_data.PaymentMethod.value,
            status=employee_data.Status.value,
            expense_account=employee_data.ExpenseAccount.value,
            expense_subaccount=employee_data.ExpenseSubaccount.value,
            identity_number=employee_data.IdentityNumber.value,
            identity_type=employee_data.IdentityType.value,
            last_modified_date_time=datetime.fromisoformat(employee_data.LastModifiedDateTime.value)
        )
        db.add(new_employee)
        db.commit()

    # Process nested relationships like Contact, Address, EmploymentHistory, PaymentInstruction, etc.
    if employee_data.Contact:
        contact_data = employee_data.Contact
        contact = Contact(
            id=contact_data.id,
            employee_id=employee_data.EmployeeID.value,
            display_name=contact_data.DisplayName.value,
            email=contact_data.Email.value,
            phone1_type=contact_data.Phone1Type.value,
            title=contact_data.Title.value
        )
        db.add(contact)
        db.commit()

        # Handle address if present
        if contact_data.Address:
            address_data = contact_data.Address
            address = Address(
                id=address_data.id,
                contact_id=contact_data.id,
                address_line1=address_data.AddressLine1.value,
                address_line2=address_data.AddressLine2.value,
                country=address_data.Country.value
            )
            db.add(address)
            db.commit()

    # Employment History
    if employee_data.EmploymentHistory:
        for history in employee_data.EmploymentHistory:
            employment_history = EmploymentHistory(
                id=history.id,
                employee_id=employee_data.EmployeeID.value,
                active=history.Active.value,
                start_date=datetime.fromisoformat(history.StartDate.value),
                position_id=history.PositionID.value,
                rehire_eligible=history.RehireEligible.value,
                terminated=history.Terminated.value,
                start_reason=history.StartReason.value
            )
            db.add(employment_history)
        db.commit()

    # Payment Instructions
    if employee_data.PaymentInstruction:
        for instruction in employee_data.PaymentInstruction:
            payment_instruction = PaymentInstruction(
                id=instruction.id,
                employee_id=employee_data.EmployeeID.value,
                b_account_id=instruction.BAccountID.value,
                description=instruction.Description.value,
                instruction_id=instruction.InstructionID.value,
                location_id=instruction.LocationID.value,
                payment_method=instruction.PaymentMethod.value,
                value=instruction.Value.value
            )
            db.add(payment_instruction)
        db.commit()

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

            # Log the raw response for debugging
            print("Raw API Response:", employee_data)

            # Validate and parse the response into the Pydantic model
            employee_response = EmployeeResponse(**employee_data)

            # Save employee data to the database
            save_employee_to_db(db, employee_response)

            return employee_response
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
