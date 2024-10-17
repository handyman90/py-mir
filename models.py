from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy database connection
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the declarative base
Base = declarative_base()

# Employee model reflecting your SQL table structure
class Employee(Base):
    __tablename__ = 'employee'  # Your table name

    row_number = Column(Integer, nullable=True)
    note = Column(String, nullable=True)
    BranchID = Column(String(30), nullable=True)
    Calendar = Column(String, nullable=True)
    CashAccount = Column(String, nullable=True)
    ContactID = Column(String(30), nullable=True)
    ContactRowNumber = Column(Integer, nullable=True)
    ContactNote = Column(String, nullable=True)
    ContactDisplayName = Column(String, nullable=True)
    ContactEmail = Column(String, nullable=True)
    ContactFax = Column(String(30), nullable=True)
    ContactFirstName = Column(String, nullable=True)
    ContactLastName = Column(String, nullable=True)
    ContactMiddleName = Column(String, nullable=True)
    ContactPhone1 = Column(String(30), nullable=True)
    ContactPhone1Type = Column(String(30), nullable=True)
    ContactPhone2 = Column(String(30), nullable=True)
    ContactPhone2Type = Column(String(30), nullable=True)
    ContactTitle = Column(String, nullable=True)
    AddressID = Column(Integer, nullable=True)
    AddressRowNumber = Column(Integer, nullable=True)
    AddressNote = Column(String, nullable=True)
    AddressLine1 = Column(String, nullable=True)
    AddressLine2 = Column(String, nullable=True)
    AddressCity = Column(String, nullable=True)
    AddressCountry = Column(String, nullable=True)
    AddressPostalCode = Column(String, nullable=True)
    AddressState = Column(String, nullable=True)
    CurrencyID = Column(String(10), nullable=True)
    DateOfBirth = Column(DateTime, nullable=True)
    DepartmentID = Column(String(30), nullable=True)
    EmployeeClassID = Column(String(10), nullable=True)
    EmployeeID = Column(String(30), nullable=True)
    EmploymentHistoryID = Column(String(30), nullable=True)
    EmploymentHistoryRowNumber = Column(Integer, nullable=True)
    EmploymentHistoryNote = Column(String, nullable=True)
    EmploymentHistoryActive = Column(Boolean, nullable=True)
    EmploymentHistoryEndDate = Column(DateTime, nullable=True)
    EmploymentHistoryLineNbr = Column(Integer, nullable=True)
    EmploymentHistoryPositionID = Column(String(10), nullable=True)
    EmploymentHistoryRehireEligible = Column(Boolean, nullable=True)
    EmploymentHistoryStartDate = Column(DateTime, nullable=True)
    EmploymentHistoryStartReason = Column(String, nullable=True)
    EmploymentHistoryTerminated = Column(Boolean, nullable=True)
    EmploymentHistoryTerminationReason = Column(String, nullable=True)
    ExpenseAccount = Column(String(10), nullable=True)
    ExpenseSubaccount = Column(String(10), nullable=True)
    IdentityNumber = Column(String(10), nullable=True)
    IdentityType = Column(String(10), nullable=True)
    LastModifiedDateTime = Column(String, nullable=True)  # Changed to String for generality
    Name = Column(String, nullable=True)
    PaymentInstructionID = Column(Integer, nullable=True)
    PaymentInstructionRowNumber = Column(Integer, nullable=True)
    PaymentInstructionNote = Column(String, nullable=True)
    PaymentInstructionBAccountID = Column(Integer, nullable=True)
    PaymentInstructionDescription = Column(String, nullable=True)
    PaymentInstructionLocationID = Column(Integer, nullable=True)
    PaymentMethod = Column(String(10), nullable=True)
    ReportsToID = Column(String(30), nullable=True)
    SalesAccount = Column(String(10), nullable=True)
    SalesSubaccount = Column(String(30), nullable=True)
    Status = Column(String(10), nullable=True)
    Custom = Column(String, nullable=True)  # Store custom fields
    Links = Column(String, nullable=True)   # Store links as JSON

# Create the database tables
Base.metadata.create_all(bind=engine)
