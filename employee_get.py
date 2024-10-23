import requests
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Fetching all employees from the server
async def fetch_employees(token: str):
    employee_data_url = "https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee"
    headers = {"Authorization": f"Bearer {token}"}

    # Assuming pagination, start with the first page
    page = 1
    while True:
        response = requests.get(f"{employee_data_url}?page={page}", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch employee data")

        data = response.json()
        employees = data.get("value", [])
        
        if not employees:
            break

        for employee_data in employees:
            if isinstance(employee_data, dict) and employee_data.get("Status", {}).get("value") == "Active":
                yield flatten_employee_data(employee_data)
        
        page += 1  # Move to the next page

# Flattening employee data
def flatten_employee_data(employee_data: dict) -> dict:
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

# Endpoint to trigger the Excel generation
@app.get("/generate_excel")
async def generate_excel():
    token = get_auth_token().get("access_token")
    employees_data = []

    async for employee in fetch_employees(token):
        employees_data.append(employee)

    # Create a DataFrame and write to Excel
    df = pd.DataFrame(employees_data)
    output_file = "employees_active.xlsx"
    df.to_excel(output_file, index=False)

    return {"message": f"Excel file '{output_file}' created successfully."}

# Serve the HTML client
@app.get("/", response_class=HTMLResponse)
async def get_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Employee Excel Generator</title>
        <script>
            async function generateExcel() {
                const response = await fetch('/generate_excel');
                const data = await response.json();
                alert(data.message);
            }
        </script>
    </head>
    <body>
        <h1>Employee Excel Generator</h1>
        <button onclick="generateExcel()">Generate Active Employees Excel</button>
    </body>
    </html>
    """
