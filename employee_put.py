from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from employee_put_models import Employee, EmployeePutModel  # Import your SQLAlchemy and Pydantic models
from models import SessionLocal  # Import session factory
from datetime import datetime

app = FastAPI()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mapping between your API fields and database fields
FIELD_MAPPING = {
    "BranchID": "branch_id",            # Map API BranchID to DB branch_id
    "CurrencyID": "currency_id",        # Map API CurrencyID to DB currency_id
    "DateOfBirth": "tkhLahir",          # Map API DateOfBirth to DB tkhLahir
    "DepartmentID": "department_id",     # Map API DepartmentID to DB department_id
    "EmployeeClassID": "employee_class_id", # Map API EmployeeClassID to DB employee_class_id
    "EmployeeID": "Nokt",               # Map API EmployeeID to DB Nokt
    "Name": "Nama",                     # Map API Name to DB Nama
    "PaymentMethod": "payment_method",   # Map API PaymentMethod to DB payment_method
    "Status": "status",                  # Map API Status to DB status
}

# PUT endpoint to update employee data based on the employee_id
@app.put("/organization/employee/{employee_id}")
def update_employee(employee_id: str, updated_employee: EmployeePutModel, db: Session = Depends(get_db)):
    # Fetch employee from the peribadi_GRP table
    employee = db.query(Employee).filter(Employee.Nokt == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Update fields using the mapping
    for api_field, db_field in FIELD_MAPPING.items():
        value = getattr(updated_employee, api_field, None)
        
        if value and value.value:  # Ensure the value exists
            if db_field == "tkhLahir":  # Special case for DateOfBirth
                setattr(employee, db_field, datetime.fromisoformat(value.value.replace("Z", "+00:00")))
            else:
                setattr(employee, db_field, value.value)

    # Commit the changes to the database
    db.commit()

    return {"message": "Employee updated successfully", "employee_id": employee.Nokt}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
