from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from sqlalchemy.orm import Session
from employee_get_models import EmployeeResponse  # Import the updated Pydantic models
from models import SessionLocal  # Your database models
from typing import Optional

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

            # Validate against the EmployeeResponse model
            employee_response = EmployeeResponse(**employee_data)

            return employee_response
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
