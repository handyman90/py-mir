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

*************************************************************************************************************************************************

To schedule a Python script (like your API) to run automatically on a Windows Server, you can use **Task Scheduler**, which is the Windows equivalent of cron jobs on Linux. Here’s how you can set up a task to run your Python API scripts every midnight.

### **Steps to Schedule a Python Script on Windows Server using Task Scheduler:**

### **1. Create a Batch File (Optional but Recommended)**
First, create a batch file (`.bat`) that will run your Python script. This batch file will be scheduled to run by the Task Scheduler.

- Open **Notepad** and create a file named `run_api.bat`.
- Inside the file, add the commands to run your Python scripts. For example:

```batch
@echo off
REM Navigate to the directory where the Python scripts are located
cd /d C:\path\to\your\scripts

REM Run the Python scripts
python employee_get.py
python employee_put.py
python payroll_get.py
python payroll_put.py

REM Exit
exit
```

Save the file as `run_api.bat`.

### **2. Open Task Scheduler**
- Open **Start** and search for **Task Scheduler**.
- Select **Task Scheduler** from the search results to open it.

### **3. Create a New Task**
1. **In Task Scheduler**, click on **Create Task** on the right side of the window.
2. **In the General tab**, name your task, e.g., "Run Python API Midnight".
   - Ensure the task is set to run **whether the user is logged in or not**.
   - Check **Run with highest privileges** to make sure the script has the permissions it needs to run.

### **4. Set the Trigger (Schedule the Task)**
1. **Go to the Triggers tab** and click **New**.
2. Set the task to start **Daily** and select the time (e.g., **00:00** for midnight).
3. Choose **Repeat every day**.

### **5. Set the Action (Run the Python Script or Batch File)**
1. **Go to the Actions tab** and click **New**.
2. In the **Action** dropdown, select **Start a program**.
3. In the **Program/script** field, either:
   - **For a batch file**: Browse to your `run_api.bat` file.
   - **For a direct Python script**: Type the path to the Python executable, e.g., `C:\path\to\python.exe`.
4. In the **Add arguments** field:
   - **For a batch file**: Leave this field blank.
   - **For a Python script**: If you're running a single script, add the path to your Python script, e.g.:
     ```bash
     C:\path\to\your\scripts\employee_get.py
     ```

5. In the **Start in (optional)** field:
   - Set the path to your script directory, e.g., `C:\path\to\your\scripts`.

### **6. Set Additional Conditions (Optional)**
- **Go to the Conditions tab** and ensure that the task is set to run whether the computer is idle or not. You may also choose to wake the computer to run this task if needed.

### **7. Set Task Settings (Optional)**
- **In the Settings tab**, you can set how to handle task failures, e.g., restart the task if it fails or stop it if it runs longer than expected.

### **8. Save the Task**
- Click **OK** to save the task.
- You may be asked for your Windows password to set up the task to run when you're not logged in. Enter the password if prompted.

### **9. Testing the Task**
You can test the task manually by selecting it in Task Scheduler and clicking **Run** from the right-side menu. This will trigger the task immediately.

### **Alternative: Directly Running Python Script Without a Batch File**
If you prefer not to use a batch file, you can directly specify the Python executable and script in the **Actions** tab of Task Scheduler:
- **Program/script**: `C:\path\to\python.exe`
- **Add arguments**: `C:\path\to\your\scripts\employee_get.py`

### **Log and Monitor the Task**
If you want to capture logs from the script, modify the batch file to output to a log file, e.g.,:

```batch
@echo off
cd /d C:\path\to\your\scripts
python employee_get.py >> api_log.txt 2>&1
python employee_put.py >> api_log.txt 2>&1
python payroll_get.py >> api_log.txt 2>&1
python payroll_put.py >> api_log.txt 2>&1
exit
```

This will log any output or errors to the `api_log.txt` file for troubleshooting.

---

### **Summary of Steps:**
1. Create a batch file (`.bat`) to run your Python scripts (optional but recommended).
2. Use **Task Scheduler** to create a new task.
3. Schedule the task to run every midnight (00:00).
4. Set the action to start your Python script or batch file.
5. Optionally, configure logging to monitor the task's output.

This method ensures your Python API scripts will run automatically every night at midnight on your Windows server.
