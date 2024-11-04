from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
import databases

# Database connection settings
DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Create an async database engine
engine = create_async_engine(DATABASE_URL, echo=True)
database = databases.Database(DATABASE_URL)

# Create metadata and define the table
metadata = MetaData()
peribadi = Table('peribadi', metadata, autoload_with=engine)

# Create FastAPI app
app = FastAPI()

# Dependency to get a database session
async def get_db():
    async with database.connection() as connection:
        yield connection

# Connect to the database on startup
@app.on_event("startup")
async def startup():
    await database.connect()

# Disconnect from the database on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Endpoint to get employee data by NoStaf
@app.get("/get_employee/{NoStaf}")
async def get_employee(NoStaf: str):
    # Execute the query
    query = select(peribadi).where(peribadi.c.NoStaf == NoStaf)
    result = await database.fetch_one(query)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Convert the Row to a dictionary manually
    employee_data = {
        "Nama": result['Nama'],
        "NoStaf": result['NoStaf'],
        "Nokt": result['Nokt'],
        "Nokpbaru": result['Nokpbaru']
    }

    return employee_data

# Run the FastAPI app with Uvicorn
# To run the app, use the command: uvicorn your_filename:app --reload
