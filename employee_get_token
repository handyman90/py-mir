# employee_get.py

from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Token URL and payload for authentication
token_url = "http://202.75.55.71/2023R1Preprod/identity/connect/token"

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

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")

# Endpoint to test the token
@app.get("/test-token")
def test_token():
    try:
        token = get_auth_token()
        return {"status": "success", "token": token}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
