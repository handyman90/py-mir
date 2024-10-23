from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from sqlalchemy.orm import Session
from models import SessionLocal, Employee, Contact
from employee_get_models import EmployeeResponse, ValueField, Contact as ContactModel, Address, EmploymentHistory, PaymentInstruction
from datetime import datetime

app = FastAPI()

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def handle_value_field(data):
    if isinstance(data, dict) and len(data) == 0:
        print("Warning: Empty dictionary encountered for ValueField. Using None.")
        return None
    return data

@app.get("/organization/employee/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id:
