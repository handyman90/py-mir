from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from employee_put_models import Employee, EmployeePutModel  # Import your SQLAlchemy model and Pydantic model
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

# PUT endpoint to update employee data based on the employee_id
@app.put("/organization/employee/{employee_id}")
def update_employee(employee_id: str, updated_employee: EmployeePutModel, db: Session = Depends(get_db)):
    # Fetch employee from the peribadi_GRP table
    employee = db.query(Employee).filter(Employee.Nokt == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Update fields
    employee.Nama = updated_employee.Nama.value or employee.Nama
    employee.tkhLahir = datetime.fromisoformat(updated_employee.tkhLahir.value.replace("Z", "+00:00")) if updated_employee.tkhLahir.value else employee.tkhLahir

    # Commit the changes to the database
    db.commit()

    return {"message": "Employee updated successfully", "employee_id": employee.Nokt}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
