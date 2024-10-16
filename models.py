from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL-encoded connection string with the updated password
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Set up the engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# SQLAlchemy model for the employee table
class Employee(Base):
    __tablename__ = 'employee'  # Table name set to 'employee'

    # Define the fields corresponding to the expected JSON response
    id = Column(String(36), primary_key=True, index=True)  # Unique identifier
    rowNumber = Column(Integer, nullable=True)  # Row number
    note = Column(String, nullable=True)  # Note field
    BranchID = Column(String(30), nullable=True)  # Branch ID
    Calendar = Column(String(30), nullable=True)  # Calendar
    CashAccount = Column(String(30), nullable=True)  # Cash Account
    CurrencyID = Column(String(10), nullable=True)  # Currency ID
    DateOfBirth = Column(DateTime, nullable=True)  # Date of Birth
    DepartmentID = Column(String(30), nullable=True)  # Department ID
    EmployeeClassID = Column(String(10), nullable=True)  # Employee Class ID
    EmployeeID = Column(String(30), nullable=True)  # Employee ID
    ExpenseAccount = Column(String(30), nullable=True)  # Expense Account
    ExpenseSubaccount = Column(String(30), nullable=True)  # Expense Subaccount
    IdentityNumber = Column(String(30), nullable=True)  # Identity Number
    IdentityType = Column(String(30), nullable=True)  # Identity Type
    LastModifiedDateTime = Column(DateTime, nullable=True)  # Last Modified DateTime
    Name = Column(String(255), nullable=True)  # Name
    PaymentMethod = Column(String(10), nullable=True)  # Payment Method
    ReportsToID = Column(String(30), nullable=True)  # Reports To ID
    SalesAccount = Column(String(30), nullable=True)  # Sales Account
    SalesSubaccount = Column(String(30), nullable=True)  # Sales Subaccount
    Status = Column(String(30), nullable=True)  # Status
    custom_fields = Column(JSON, nullable=True)  # Store custom fields as JSON
    links = Column(JSON, nullable=True)  # Store links as JSON

# Create the database tables
Base.metadata.create_all(bind=engine)
 
