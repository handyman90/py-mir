To run the provided FastAPI code on your server, you need to modify the following parts of the code:

### 1. **Update the Base URL for Authentication and API Requests**

Change the placeholder URL (`https://example.com/entity/`) to the actual URL of your server where the API endpoints reside.

- **In both `employee_get.py`, `employee_put.py`, `payroll_get.py`, and `payroll_put.py`:**

   ```python
   token_url = "https://yourserver.com/entity/auth/login"
   ```

- **For GET and PUT requests:**

   ```python
   url = f"https://yourserver.com/entity/GRP9Default/1/Employee?$filter=EmployeeID eq '{employee_id}'"
   ```

   and

   ```python
   url = "https://yourserver.com/entity/GRP9Default/1/Employee"
   ```

### 2. **Update Authentication Credentials**

Ensure the credentials used for authentication (`name`, `password`, `company`) match the ones required by your server's API.

- **In the `get_auth_token` function:**

   ```python
   payload = {
       "name": "your_username",
       "password": "your_password",
       "company": "YourCompany"
   }
   ```

### 3. **Adjust the Host and Port (Optional)**

If you need to change the host and port to match your server's configuration, update the `uvicorn.run` command at the bottom of each file.

- **In each of the Python files (`employee_get.py`, `employee_put.py`, `payroll_get.py`, `payroll_put.py`) at the bottom:**

   ```python
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port if needed
   ```

   - **`host="0.0.0.0"`**: This allows the app to be accessible externally. You can set it to `"127.0.0.1"` if you want it to be accessible only locally.
   - **`port=8000`**: Change this to the desired port number if your server uses a different one.

### 4. **Install Necessary Dependencies**

Make sure you have the necessary Python packages installed on your server. You can install them using:

```bash
pip install fastapi uvicorn pydantic requests
```

### 5. **Run the API**

After making the above changes, you can start the API on your server by running the Python files:

```bash
python employee_get.py
python employee_put.py
python payroll_get.py
python payroll_put.py
```

This will start the FastAPI server, and your endpoints will be available at the specified host and port.

### Summary:

- **Base URL**: Update the URLs to match your server.
- **Authentication**: Use the correct credentials.
- **Host and Port**: Adjust if necessary.
- **Dependencies**: Ensure all required packages are installed.
  
These steps will ensure that the API is correctly configured to run on your server.
