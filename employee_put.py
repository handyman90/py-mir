# employee_put.py

import requests
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Dict
import json

# Constants for API endpoints and credentials
TOKEN_URL = "https://csmstg.censof.com/2023R1Preprod/identity/connect/token"
EMPLOYEE_URL = "https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee"
CLIENT_ID = "03407458-3136-511B-24FB-68D470104D22@MIROS 090624"
CLIENT_SECRET = "3gVM0RbnqDwXYfO1aekAyw"
USERNAME = "apiuser"
PASSWORD = "apiuser"
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Database setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Define the FastAPI application
app = FastAPI()

# Authentication function
def get_auth_token() -> str:
    payload = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api",
        "username": USERNAME,
        "password": PASSWORD
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

# Function to convert a database row to JSON
def row_to_json(row) -> Dict:
    return {
        "EmployeeID": {"value": str(row.EmployeeID)},
        "EmployeeClassID": {"value": row.EmployeeClassID},
        "BranchID": {"value": row.BranchID},
        "DepartmentID": {"value": row.DepartmentID},
        "Calendar": {"value": row.Calendar},
        "DateOfBirth": {"value": row.DateOfBirth.strftime('%Y-%m-%d')},
        "IdentityType": {"value": row.IdentityType},
        "IdentityNumber": {"value": row.IdentityNumber},
        "PaymentMethod": {"value": row.PaymentMethod},
        "CashAccount": {"value": row.CashAccount},
        "Status": {"value": row.Status},
        "Contact": {
            "LastName": {"value": row.LastName},
            "Phone1": {"value": row.Phone1},
            "Phone2": {"value": row.Phone2},
            "Email": {"value": row.Email},
            "Address": {
                "AddressLine1": {"value": row.AddressLine1},
                "AddressLine2": {"value": row.AddressLine2},
                "City": {"value": row.City},
                "Country": {"value": row.Country},
                "PostalCode": {"value": row.PostalCode},
                "State": {"value": row.State}
            }
        },
        "EmploymentHistory": [
            {
                "Active": {"value": row.Active},
                "PositionID": {"value": row.PositionID},
                "StartDate": {"value": row.StartDate.strftime('%Y-%m-%d')}
            }
        ]
    }

# Function to submit employee data to GRP
def submit_advance_data(data: Dict, token: str) -> Dict:
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(EMPLOYEE_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Submission failed: {response.status_code}, {response.text}")

# Endpoint to trigger data sending
@app.get("/send_employee_data")
def send_employee_data():
    token = get_auth_token()  # Retrieve the session token
    conn = engine.connect()
    employee_table = Table("Employee", metadata, autoload_with=engine)

    select_query = select(employee_table)
    results = conn.execute(select_query)

    response_list = []
    for row in results:
        try:
            json_data = row_to_json(row)  # Convert row to JSON format
            response = submit_advance_data(json_data, token)  # Send data
            response_list.append({"EmployeeID": row.EmployeeID, "status": "Success", "response": response})
        except Exception as e:
            response_list.append({"EmployeeID": row.EmployeeID, "status": "Error", "message": str(e)})

    conn.close()
    return response_list
