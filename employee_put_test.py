import requests
import json
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import sessionmaker
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection string
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Setup the database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create MetaData instance
metadata = MetaData()

# Reflect the table structure for "peribadi"
try:
    peribadi = Table("peribadi", metadata, autoload_with=engine)
    logger.info("Table structure reflected successfully.")
except Exception as e:
    logger.error(f"Error reflecting table structure: {e}")
    raise

# FastAPI instance
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/get_employee/{no_staf}")
async def get_employee(no_staf: str, db=Depends(get_db)):
    try:
        logger.info(f"Fetching employee data for NoStaf: {no_staf}")
        # Select specific columns from the "peribadi" table
        stmt = select(
            peribadi.c.NoStaf, peribadi.c.EmployeeClassID, peribadi.c.BranchID,
            peribadi.c.DepartmentID, peribadi.c.tkhLahir, peribadi.c.Nokpbaru,
            peribadi.c.Carapembayaran, peribadi.c.CashAccount, peribadi.c.Status_grp,
            peribadi.c.LastName_grp, peribadi.c.TelefonB, peribadi.c.EMAIL,
            peribadi.c.Alamat1, peribadi.c.Alamat2, peribadi.c.BANDAR, peribadi.c.Poskod,
            peribadi.c.NEGERI, peribadi.c.Active_grp, peribadi.c.PositionID_grp,
            peribadi.c.startdate_grp
        ).where(peribadi.c.NoStaf == no_staf)
        result = db.execute(stmt).fetchone()  # Fetch one record
        if result:
            logger.info(f"Employee data fetched successfully for NoStaf: {no_staf}")
            # Map the database columns to the expected JSON structure
            employee = {
                "EmployeeID": {"value": result[0].strip() if result[0] else None},  # NoStaf
                "EmployeeClassID": {"value": result[1].strip() if result[1] else None},  # EmployeeClassID
                "BranchID": {"value": result[2].strip() if result[2] else None},  # BranchID
                "DepartmentID": {"value": result[3].strip() if result[3] else None},  # DepartmentID
                "Calendar": {"value": "NORMAL"},  # Assuming a default value
                "DateOfBirth": {"value": result[4].strftime('%Y-%m-%d') if result[4] else None},  # tkhLahir
                "IdentityType": {"value": "New IC No."},  # Assuming a default value
                "IdentityNumber": {"value": result[5].strip() if result[5] else None},  # Nokpbaru
                "PaymentMethod": {"value": result[6].strip() if result[6] else None},  # Carapembayaran
                "CashAccount": {"value": result[7].strip() if result[7] else None},  # CashAccount
                "Status": {"value": result[8].strip() if result[8] else None},  # Status_grp
                "Contact": {
                    "LastName": {"value": result[9].strip() if result[9] else None},  # LastName_grp
                    "Phone1": {"value": result[10].strip() if result[10] else None},  # TelefonB
                    "Phone2": {"value": result[10].strip() if result[10] else None},  # TelefonB
                    "Email": {"value": result[11].strip() if result[11] else None},  # EMAIL
                    "Address": {
                        "AddressLine1": {"value": result[12].strip() if result[12] else None},  # Alamat1
                        "AddressLine2": {"value": result[13].strip() if result[13] else None},  # Alamat2
                        "City": {"value": result[14].strip() if result[14] else None},  # BANDAR
                        "Country": {"value": "MY"},  # Assuming a default value
                        "PostalCode": {"value": result[15].strip() if result[15] else None},  # Poskod
                        "State": {"value": result[16].strip() if result[16] else None}  # NEGERI
                    }
                },
                "EmploymentHistory": [
                    {
                        "Active": {"value": result[17] if result[17] else None},  # Active_grp
                        "PositionID": {"value": result[18].strip() if result[18] else None},  # PositionID_grp
                        "StartDate": {"value": result[19].strftime('%Y-%m-%d') if result[19] else None}  # startdate_grp
                    }
                ]
            }

            # Send PUT request to the external API
            url = "https://csmstg.censof.com/2023R1Preprod/entity/GRP9Default/1/Employee"
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.put(url, headers=headers, data=json.dumps(employee))

            if response.status_code == 200:
                logger.info(f"Successfully sent PUT request for NoStaf: {no_staf}")
                return {"message": "Employee data sent successfully", "response": response.json()}
            else:
                logger.error(f"Failed to send PUT request for NoStaf: {no_staf}. Status code: {response.status_code}, Response: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
        else:
            logger.warning(f"Employee not found for NoStaf: {no_staf}")
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        logger.error(f"Error fetching employee data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# To run the application, use the following command:
# uvicorn employee_put:app --reload
