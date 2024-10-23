from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import requests
import pandas as pd
import os
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

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

# Initialize progress tracking
progress = {"current": 0, "total": 0}

def fetch_employee_data():
    global progress
    progress["current"] = 0

    # Get the authentication token
    try:
        token_data = get_auth_token()
        access_token = token_data["access_token"]
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return

    # Endpoint to retrieve employee IDs
    ids_endpoint = "https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee"
    
    # Fetching all employee IDs
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(ids_endpoint, headers=headers)
    
    if response.status_code != 200:
        logging.error(f"Failed to fetch employee IDs: {response.status_code} - {response.text}")
        return

    employee_ids = [emp['id'] for emp in response.json()]

    # Filter employee IDs based on your criteria
    filtered_employee_ids = [emp_id for emp_id in employee_ids if emp_id.startswith(('MIP', 'FEL', 'MIS', 'PSH'))]

    # Update progress total
    progress["total"] = len(filtered_employee_ids)

    # Prepare the data for Excel
    flattened_employees = []

    # Clear existing Excel file if it exists
    excel_file_path = "employees.xlsx"
    if os.path.exists(excel_file_path):
        os.remove(excel_file_path)

    for emp_id in filtered_employee_ids:
        emp_endpoint = f"https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee/{emp_id}"
        emp_response = requests.get(emp_endpoint, headers=headers)
        
        if emp_response.status_code == 200:
            employee_data = emp_response.json()
            # Ensure that we only write Active employees to Excel
            if employee_data.get("Status", {}).get("value") == "Active":
                flattened_emp = {
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
                    "AddressCity": employee_data.get("Contact", {}).get("Address", {}).get("City", {}).get("value"),
                    "AddressCountry": employee_data.get("Contact", {}).get("Address", {}).get("Country", {}).get("value"),
                    "AddressPostalCode": employee_data.get("Contact", {}).get("Address", {}).get("PostalCode", {}).get("value"),
                    "AddressState": employee_data.get("Contact", {}).get("Address", {}).get("State", {}).get("value"),
                    # Flatten EmploymentHistory
                    "EmploymentHistoryPositionID": employee_data.get("EmploymentHistory", [{}])[0].get("PositionID", {}).get("value"),
                    "EmploymentHistoryStartDate": employee_data.get("EmploymentHistory", [{}])[0].get("StartDate", {}).get("value"),
                    "EmploymentHistoryEndDate": employee_data.get("EmploymentHistory", [{}])[0].get("EndDate", {}).get("value"),
                    # Flatten PaymentInstruction
                    "PaymentInstructionValue": employee_data.get("PaymentInstruction", [{}])[0].get("Value", {}).get("value"),
                }
                flattened_employees.append(flattened_emp)
                progress["current"] += 1
        else:
            logging.error(f"Failed to fetch data for employee ID {emp_id}: {emp_response.status_code} - {emp_response.text}")

    # Write to Excel only if data is available
    if flattened_employees:
        df = pd.DataFrame(flattened_employees)
        df.to_excel(excel_file_path, index=False)
    else:
        logging.info("No active employees found for the specified filters.")

@app.get("/fetch_employees")
async def fetch_employees(background_tasks: BackgroundTasks):
    background_tasks.add_task(fetch_employee_data)
    return JSONResponse(content={"message": "Fetching employee data in the background."})

@app.get("/progress")
async def get_progress():
    return JSONResponse(content=progress)
