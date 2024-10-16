from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from sqlalchemy.orm import Session
from models import Employee, SessionLocal, Base, engine
from employee_get_models import EmployeeResponse
from datetime import datetime

app = FastAPI()

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

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

# Endpoint to retrieve and save employee information
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

            # Create or update employee record in the database
            existing_employee = db.query(Employee).filter(Employee.id == employee_data["EmployeeID"]["value"]).first()
            
            if existing_employee:
                # Update existing employee logic here...
                pass  # Update logic goes here
            else:
                # Create a new employee record logic here...
                pass  # Create logic goes here

            # Convert boolean and integer fields to strings if necessary
            for history in employee_data.get("EmploymentHistory", []):
                history['Active'] = {'value': str(history['Active']['value'])}  # Convert bool to string
                history['LineNbr'] = {'value': str(history['LineNbr']['value'])}  # Convert int to string
                history['RehireEligible'] = {'value': str(history['RehireEligible']['value'])}  # Convert bool to string
                history['Terminated'] = {'value': str(history['Terminated']['value'])}  # Convert bool to string

            for payment in employee_data.get("PaymentInstruction", []):
                payment['BAccountID'] = {'value': str(payment['BAccountID']['value'])}  # Convert int to string
                payment['LocationID'] = {'value': str(payment['LocationID']['value'])}  # Convert int to string

            # Directly unpacking the response to the model
            return EmployeeResponse(**employee_data)

        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Set to 0.0.0.0 to accept requests from any IP
