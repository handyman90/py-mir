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

# Mapping between your database fields and API fields
FIELD_MAPPING = {
    "Nokt": "EmployeeID",
    "Nama": "Name",
    "tkhLahir": "DateOfBirth",
}

# PUT endpoint to update employee data based on the employee_id
@app.put("/organization/employee/{employee_id}")
def update_employee(employee_id: str, updated_employee: EmployeePutModel, db: Session = Depends(get_db)):
    # Fetch employee from the peribadi_GRP table
    employee = db.query(Employee).filter(Employee.Nokt == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Update fields using the mapping
    for db_field, api_field in FIELD_MAPPING.items():
        value = getattr(updated_employee, db_field).value if hasattr(updated_employee, db_field) else None
        if value:
            if db_field == "tkhLahir":
                value = datetime.fromisoformat(value.replace("Z", "+00:00"))  # Convert to datetime
            setattr(employee, db_field, value)  # Update the employee model field

    # Commit the changes to the database
    db.commit()

    return {"message": "Employee updated successfully", "employee_id": employee.Nokt}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
