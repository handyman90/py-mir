from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(String, primary_key=True, index=True)  # Employee's unique ID (UUID format)
    row_number = Column(Integer, nullable=True)  # rowNumber from JSON
    note = Column(String, nullable=True)  # note field
    branch_id = Column(String, nullable=True)  # BranchID
    contact_id = Column(String, nullable=True)  # Contact ID
    contact_email = Column(String, nullable=True)  # Contact Email
    contact_first_name = Column(String, nullable=True)  # Contact FirstName
    contact_last_name = Column(String, nullable=True)  # Contact LastName
    contact_phone1 = Column(String, nullable=True)  # Contact Phone1
    contact_phone2 = Column(String, nullable=True)  # Contact Phone2
    contact_title = Column(String, nullable=True)  # Contact Title
    currency_id = Column(String, nullable=True)  # CurrencyID
    date_of_birth = Column(DateTime, nullable=True)  # DateOfBirth
    department_id = Column(String, nullable=True)  # DepartmentID
    employee_class_id = Column(String, nullable=True)  # EmployeeClassID
    employee_cost = Column(JSON, nullable=True)  # Store EmployeeCost as JSON
    employment_history = Column(JSON, nullable=True)  # Store EmploymentHistory as JSON
    status = Column(String, nullable=True)  # Employee status
    custom_fields = Column(JSON, nullable=True)  # Store custom fields as JSON

# Database connection string (update with your own credentials)
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://username:password@server/dbname?driver=ODBC+Driver+17+for+SQL+Server"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
