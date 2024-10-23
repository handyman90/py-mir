from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import pandas as pd
import time
from fastapi import BackgroundTasks
from starlette.responses import StreamingResponse

app = FastAPI()

# Allow CORS for all origins
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
def get_auth_token() -> str:
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
        return response.json().get("access_token")
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

# HTML template for progress
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Data Export</title>
</head>
<body>
    <h1>Exporting Employee Data to Excel</h1>
    <button id="start-btn">Start Export</button>
    <div id="progress"></div>
    <script>
        document.getElementById("start-btn").onclick = function() {
            fetch("/export")
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                const reader = response.body.getReader();
                const total = 100;  // Assuming total steps for demonstration
                let progress = 0;

                const updateProgress = () => {
                    reader.read().then(({ done, value }) => {
                        if (done) return;
                        progress += value[0];  // Simulated progress increment
                        document.getElementById("progress").innerText = `Progress: ${progress}%`;
                        if (progress < total) {
                            updateProgress();
                        } else {
                            document.getElementById("progress").innerText = 'Export Complete! Download here: <a href="/download">Download Excel</a>';
                        }
                    });
                };

                updateProgress();
            })
            .catch(error => console.error('Error:', error));
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_TEMPLATE

@app.get("/export")
async def export_employees(background_tasks: BackgroundTasks):
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch the employee IDs
    employee_ids = []
    response = requests.get("https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee", headers=headers)

    if response.status_code == 200:
        data = response.json()
        employee_ids = [emp['id'] for emp in data if emp.get("Status") == "Active"]  # Filter for active employees
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch employee data")

    # Prepare for Excel writing
    all_employees_data = []
    total_employees = len(employee_ids)

    # Loop through each employee ID and fetch details
    for idx, employee_id in enumerate(employee_ids):
        employee_response = requests.get(f"https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee/{employee_id}", headers=headers)
        
        if employee_response.status_code == 200:
            employee_data = employee_response.json()
            # Only add if employee is Active
            if employee_data.get("Status") == "Active":
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
                    "ContactID": employee_data.get("Contact", {}).get("id"),
                    "ContactDisplayName": employee_data.get("Contact", {}).get("DisplayName", {}).get("value"),
                    "ContactEmail": employee_data.get("Contact", {}).get("Email", {}).get("value"),
                    "AddressLine1": employee_data.get("Contact", {}).get("Address", {}).get("AddressLine1", {}).get("value"),
                    "AddressLine2": employee_data.get("Contact", {}).get("Address", {}).get("AddressLine2", {}).get("value"),
                    "AddressCity": employee_data.get("Contact", {}).get("Address", {}).get("City", {}),
                    "AddressCountry": employee_data.get("Contact", {}).get("Address", {}).get("Country", {}).get("value"),
                    "AddressPostalCode": employee_data.get("Contact", {}).get("Address", {}).get("PostalCode", {}),
                    "AddressState": employee_data.get("Contact", {}).get("Address", {}).get("State", {}),
                    "EmploymentHistoryPositionID": employee_data.get("EmploymentHistory", [{}])[0].get("PositionID", {}).get("value"),
                    "EmploymentHistoryStartDate": employee_data.get("EmploymentHistory", [{}])[0].get("StartDate", {}).get("value"),
                    "EmploymentHistoryEndDate": employee_data.get("EmploymentHistory", [{}])[0].get("EndDate", {}),
                    "PaymentInstructionValue": employee_data.get("PaymentInstruction", [{}])[0].get("Value", {}).get("value"),
                }
                all_employees_data.append(flattened_emp)

        # Simulating progress
        time.sleep(0.1)  # Simulate processing time
        progress = (idx + 1) / total_employees * 100
        yield f"{progress}\n"  # Send progress update

    # Write to Excel after collecting all active employees
    df = pd.DataFrame(all_employees_data)
    output_file = "active_employees.xlsx"
    df.to_excel(output_file, index=False)

    background_tasks.add_task(lambda: print(f"Exported {len(all_employees_data)} active employees to {output_file}"))

    return {"message": "Export complete. You can download the file."}
