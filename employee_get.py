# employee_get.py

from fastapi import FastAPI, HTTPException
import json
import requests

app = FastAPI()

# Load the JSON file (employee data)
with open('employee_data.json', 'r') as file:
    employee_data = json.load(file)

# Token URL and payload for authentication
token_url = "http://202.75.55.71/2023R1Preprod/identity/connect/token"

# Function to authenticate and get a session token
def get_auth_token():
    # Define the payload for authentication (raw payload converted to a dictionary)
    payload = {
        "grant_type": "password",
        "client_id": "03407458-3136-511B-24FB-68D470104D22@MIROS 090624",
        "client_secret": "3gVM0RbnqDwXYfO1aekAyw",
        "scope": "api",
        "username": "apiuser",
        "password": "apiuser"
    }

    # Set headers for the request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Make the POST request to get the token
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        # Extract the token from the response
        token = response.json().get('access_token')
        return token
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

@app.get("/organization/employee")
def get_employee(employee_id: str):
    # Authenticate and get the token
    token = get_auth_token()

    # If token is available, proceed with retrieving employee data
    if token:
        # Filter the data based on employee ID
        employee = next((emp for emp in employee_data if emp["EmployeeID"] == employee_id), None)
        
        if employee:
            return employee
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    else:
        raise HTTPException(status_code=401, detail="Authentication token not found")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
