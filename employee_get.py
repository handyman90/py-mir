from fastapi import FastAPI, HTTPException, Header, Depends
import requests
from employee_get_models import EmployeeResponse, ValueField, Contact, Address, EmploymentHistory, PaymentInstruction
from pandas import DataFrame
from datetime import datetime
import pandas as pd

app = FastAPI()

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

# Helper function to flatten the nested JSON
def flatten_employee_data(employee_data: dict) -> dict:
    flattened_data = {
        "id": employee_data.get("id"),
        "rowNumber": employee_data.get("rowNumber"),
        "note": employee_data.get("note"),
        "BranchID": employee_data.get("BranchID", {}).get("value"),
        "Calendar": employee_data.get("Calendar", {}).get("value"),
        "CashAccount": employee_data.get("CashAccount", {}).get("value"),
        "CurrencyID": employee_data.get("CurrencyID", {}).get("value"),
        "DateOfBirth": employee_data.get("DateOfBirth", {}).get("value"),
        "DepartmentID": employee_data.get("DepartmentID", {}).get("value"),
        "EmployeeClassID": employee_data.get("EmployeeClassID", {}).get("value"),
        "EmployeeID": employee_data.get("EmployeeID", {}).get("value"),
        "ExpenseAccount": employee_data.get("ExpenseAccount", {}).get("value"),
        "ExpenseSubaccount": employee_data.get("ExpenseSubaccount", {}).get("value"),
        "IdentityNumber": employee_data.get("IdentityNumber", {}).get("value"),
        "IdentityType": employee_data.get("IdentityType", {}).get("value"),
        "LastModifiedDateTime": employee_data.get("LastModifiedDateTime"),
        "Name": employee_data.get("Name", {}).get("value"),
        "PaymentMethod": employee_data.get("PaymentMethod", {}).get("value"),
        "Status": employee_data.get("Status", {}).get("value"),
        # Flatten Contact
        "ContactID": employee_data.get("Contact", {}).get("id"),
        "ContactDisplayName": employee_data.get("Contact", {}).get("DisplayName", {}).get("value"),
        "ContactEmail": employee_data.get("Contact", {}).get("Email", {}).get("value"),
        # Flatten Address
        "AddressLine1": employee_data.get("Contact", {}).get("Address", {}).get("AddressLine1", {}).get("value"),
        "AddressLine2": employee_data.get("Contact", {}).get("Address", {}).get("AddressLine2", {}).get("value"),
        "AddressCity": employee_data.get("Contact", {}).get("Address", {}).get("City", {}),
        "AddressCountry": employee_data.get("Contact", {}).get("Address", {}).get("Country", {}).get("value"),
        "AddressPostalCode": employee_data.get("Contact", {}).get("Address", {}).get("PostalCode", {}),
        "AddressState": employee_data.get("Contact", {}).get("Address", {}).get("State", {}),
        # Flatten EmploymentHistory
        "EmploymentHistoryPositionID": employee_data.get("EmploymentHistory", [{}])[0].get("PositionID", {}).get("value"),
        "EmploymentHistoryStartDate": employee_data.get("EmploymentHistory", [{}])[0].get("StartDate", {}).get("value"),
        "EmploymentHistoryEndDate": employee_data.get("EmploymentHistory", [{}])[0].get("EndDate", {}),
        # Flatten PaymentInstruction
        "PaymentInstructionValue": employee_data.get("PaymentInstruction", [{}])[0].get("Value", {}).get("value"),
    }
    return flattened_data

# Endpoint to retrieve and save employee information as Excel
@app.get("/organization/employee/{employee_id}")
def get_employee(employee_id: str, authorization: str = Header(None)):
    try:
        if authorization is None:
            token_response = get_auth_token()
            authorization = token_response.get("access_token")

        url = f"https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee/{employee_id}?$expand=Contact/Address,EmploymentHistory,PaymentInstruction"
        headers = {"Authorization": f"Bearer {authorization}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            employee_data = response.json()

            # Flatten the employee data
            flattened_employee = flatten_employee_data(employee_data)

            # Create a DataFrame and export to Excel
            df = DataFrame([flattened_employee])
            file_name = f"employee_{employee_id}.xlsx"
            df.to_excel(file_name, index=False)

            return {"detail": f"Employee data saved to {file_name}"}

        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching employee data")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
