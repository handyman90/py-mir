from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData

# Database connection string
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Setup the database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData(bind=engine)

# Reflect the table structure
peribadi_GRP = Table("peribadi_GRP", metadata, autoload_with=engine)

# FastAPI instance
app = FastAPI()

@app.get("/get_employee/{no_staf}")
async def get_employee(no_staf: str, db=Depends(get_db)):
    try:
        stmt = select(peribadi_GRP).where(peribadi_GRP.c.NoStaf == no_staf)
        result = db.execute(stmt).fetchone()  # Fetch one record
        if result:
            return dict(result)  # Return the record as a dictionary
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
