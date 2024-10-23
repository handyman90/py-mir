import httpx
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Fetch employee data from the server
async def fetch_employees():
    url = "https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

# Flatten employee data
def flatten_employee_data(employee_data):
    flattened_data = []

    for emp in employee_data:
        flattened_emp = {
            "id": emp.get("id"),
            "rowNumber": emp.get("rowNumber"),
            "note": emp.get("note"),
            "BranchID": emp.get("BranchID", {}).get("value"),
            "Calendar": emp.get("Calendar", {}).get("value"),
            "CashAccount": emp.get("CashAccount", {}).get("value"),
            "CurrencyID": emp.get("CurrencyID", {}).get("value"),
            "DateOfBirth": emp.get("DateOfBirth", {}).get("value"),
            "DepartmentID": emp.get("DepartmentID", {}).get("value"),
            "EmployeeClassID": emp.get("EmployeeClassID", {}).get("value"),
            "EmployeeID": emp.get("EmployeeID", {}).get("value"),
            "ExpenseAccount": emp.get("ExpenseAccount", {}).get("value"),
            "ExpenseSubaccount": emp.get("ExpenseSubaccount", {}).get("value"),
            "IdentityNumber": emp.get("IdentityNumber", {}).get("value"),
            "IdentityType": emp.get("IdentityType", {}).get("value"),
            "LastModifiedDateTime": emp.get("LastModifiedDateTime"),
            "Name": emp.get("Name", {}).get("value"),
            "PaymentMethod": emp.get("PaymentMethod", {}).get("value"),
            "Status": emp.get("Status", {}).get("value"),
            # Flatten Contact
            "ContactID": emp.get("Contact", {}).get("id"),
            "ContactDisplayName": emp.get("Contact", {}).get("DisplayName", {}).get("value"),
            "ContactEmail": emp.get("Contact", {}).get("Email", {}).get("value"),
            # Flatten Address
            "AddressLine1": emp.get("Contact", {}).get("Address", {}).get("AddressLine1", {}).get("value"),
            "AddressLine2": emp.get("Contact", {}).get("Address", {}).get("AddressLine2", {}).get("value"),
            "AddressCity": emp.get("Contact", {}).get("Address", {}).get("City"),
            "AddressCountry": emp.get("Contact", {}).get("Address", {}).get("Country", {}).get("value"),
            "AddressPostalCode": emp.get("Contact", {}).get("Address", {}).get("PostalCode"),
            "AddressState": emp.get("Contact", {}).get("Address", {}).get("State"),
            # Flatten EmploymentHistory
            "EmploymentHistoryPositionID": emp.get("EmploymentHistory", [{}])[0].get("PositionID", {}).get("value"),
            "EmploymentHistoryStartDate": emp.get("EmploymentHistory", [{}])[0].get("StartDate", {}).get("value"),
            "EmploymentHistoryEndDate": emp.get("EmploymentHistory", [{}])[0].get("EndDate"),
            # Flatten PaymentInstruction
            "PaymentInstructionValue": emp.get("PaymentInstruction", [{}])[0].get("Value", {}).get("value"),
        }
        flattened_data.append(flattened_emp)

    return flattened_data

# Save data to Excel
def save_to_excel(data, filename="employees.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# Endpoint to trigger fetching and saving employee data
@app.get("/fetch_employees")
async def fetch_and_save_employees():
    employee_json = await fetch_employees()
    flattened_data = flatten_employee_data(employee_json)
    save_to_excel(flattened_data)
    return {"message": "Employee data fetched and saved to Excel."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
