from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
import requests
import pandas as pd
import os
import logging
import time

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
progress = {"current": 0, "total": 0, "last_update_time": time.time()}

def fetch_employee_data():
    global progress
    progress["current"] = 0
    progress["last_update_time"] = time.time()  # Reset the update time

    # Get the authentication token
    try:
        token_data = get_auth_token()
        access_token = token_data["access_token"]
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return

    # Endpoint to retrieve employee data
    ids_endpoint = "https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee"
    
    # Fetching all employee data
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(ids_endpoint, headers=headers)
    
    if response.status_code != 200:
        logging.error(f"Failed to fetch employee data: {response.status_code} - {response.text}")
        return

    employee_data_list = response.json()
    logging.debug(f"Received employee data: {employee_data_list}")  # Debug logging

    # Extract EmployeeID for filtering
    employee_ids = [
        emp['EmployeeID']['value'] 
        for emp in employee_data_list 
        if 'EmployeeID' in emp and isinstance(emp['EmployeeID'], dict) and 'value' in emp['EmployeeID']
    ]

    logging.info(f"Fetched {len(employee_ids)} EmployeeIDs: {employee_ids}")  # Log all fetched EmployeeIDs

    # Filter employee IDs based on your criteria
    filtered_employee_ids = [
        emp_id 
        for emp_id in employee_ids 
        if isinstance(emp_id, str) and emp_id.startswith(('MIP', 'FEL', 'MIS', 'PSH'))
    ]

    # Update progress total to the number of filtered employee IDs
    progress["total"] = len(filtered_employee_ids)
    progress["last_update_time"] = time.time()  # Update the time after setting total

    # Log filtered results
    logging.info(f"Filtered {len(filtered_employee_ids)} EmployeeIDs matching the criteria: {filtered_employee_ids}")

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
                    "EmployeeID": employee_data.get("EmployeeID", {}).get("value"),
                    "rowNumber": employee_data.get("rowNumber"),
                    "note": employee_data.get("note"),
                    "BranchID": employee_data.get("BranchID", {}).get("value"),
                    "Calendar": employee_data.get("Calendar", {}).get("value"),
                    "CashAccount": employee_data.get("CashAccount", {}).get("value"),
                    "CurrencyID": employee_data.get("CurrencyID", {}).get("value"),
                    "DateOfBirth": employee_data.get("DateOfBirth", {}).get("value"),
                    "DepartmentID": employee_data.get("DepartmentID", {}).get("value"),
                    "EmployeeClassID": employee_data.get("EmployeeClassID", {}).get("value"),
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
                progress["current"] += 1  # Increment current progress only for processed filtered employees
                progress["last_update_time"] = time.time()  # Update the timestamp on each progress update
        else:
            logging.error(f"Failed to fetch data for EmployeeID {emp_id}: {emp_response.status_code} - {emp_response.text}")

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
    # Check if progress has stalled for more than 30 seconds
    if time.time() - progress["last_update_time"] > 30:
        progress["current"] = progress["total"]  # Mark progress as 100% if stalled
    return JSONResponse(content=progress)

@app.get("/progress_page", response_class=HTMLResponse)
async def progress_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Progress Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            .progress {
                width: 100%;
                background-color: #ccc;
                height: 30px;
                border-radius: 5px;
                overflow: hidden;
                margin-bottom: 10px;
            }
            .progress-bar {
                height: 100%;
                background-color: #76c7c0;
                transition: width 0.5s;
            }
            #status {
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Employee Data Fetch Progress</h1>
        <div class="progress" id="progress">
            <div class="progress-bar" id="progress-bar" style="width: 0%;"></div>
        </div>
        <div id="status">Fetching data...</div>
        <script>
            async function updateProgress() {
                const response = await fetch("/progress");
                const data = await response.json();
                const progressBar = document.getElementById("progress-bar");
                const status = document.getElementById("status");

                if (data.total > 0) {
                    const percentage = (data.current / data.total) * 100;
                    progressBar.style.width = percentage + '%';
                    status.innerText = `Processed ${data.current} of ${data.total} records.`;
                } else {
                    progressBar.style.width = '100%';
                    status.innerText = "No records to process.";
                }

                // Stop updating if finished
                if (data.current < data.total) {
                    setTimeout(updateProgress, 1000);
                } else {
                    status.innerText = "Data fetching complete!";
                }
            }

            updateProgress();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
