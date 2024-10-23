import requests
from fastapi import FastAPI, HTTPException
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

# Function to flatten employee data
def flatten_employee_data(employee_data):
    return {
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

# Function to save data to an Excel file
def save_to_excel(employee_data):
    df = pd.DataFrame(employee_data)
    df.to_excel("employee_data.xlsx", index=False)

@app.get("/fetch_employees")
async def fetch_employees():
    token = get_auth_token().get("access_token")
    
    # Initialize an empty list to store all employee data
    all_employees = []
    
    page = 1
    while True:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Fetch employee data from the API
        response = requests.get(f"https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/{page}/Employee", headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch employee data")

        # Get employee data from the response
        employee_data_list = response.json()
        
        # If there are no more employees, break the loop
        if not employee_data_list:
            break
        
        # Flatten and append each employee's data to the all_employees list
        for employee_data in employee_data_list:
            flattened_emp = flatten_employee_data(employee_data)
            all_employees.append(flattened_emp)
        
        page += 1  # Move to the next page
    
    # Write all employee data to Excel
    save_to_excel(all_employees)

    return {"message": "Employee data fetched and saved to Excel."}
