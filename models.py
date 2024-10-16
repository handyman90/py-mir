from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (make sure to use the correct password format)
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/employee?driver=ODBC+Driver+17+for+SQL+Server"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Employee model
class Employee(Base):
    __tablename__ = 'employee'

    id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    BranchID = Column(String(30), nullable=True)  # BranchID
    Calendar = Column(String(30), nullable=True)  # Calendar
    CashAccount = Column(String(30), nullable=True)  # CashAccount
    ContactID = Column(String(36), nullable=True)  # Contact ID
    ContactRowNumber = Column(Integer, nullable=True)  # Contact row number
    ContactNote = Column(String, nullable=True)  # Contact note
    ContactDisplayName = Column(String, nullable=True)  # Contact display name
    ContactEmail = Column(String, nullable=True)  # Contact email
    ContactFax = Column(String, nullable=True)  # Contact fax
    ContactFirstName = Column(String, nullable=True)  # Contact first name
    ContactLastName = Column(String, nullable=True)  # Contact last name
    ContactMiddleName = Column(String, nullable=True)  # Contact middle name
    ContactPhone1 = Column(String, nullable=True)  # Contact phone 1
    ContactPhone1Type = Column(String, nullable=True)  # Contact phone 1 type
    ContactPhone2 = Column(String, nullable=True)  # Contact phone 2
    ContactPhone2Type = Column(String, nullable=True)  # Contact phone 2 type
    ContactTitle = Column(String, nullable=True)  # Contact title
    AddressID = Column(String(36), nullable=True)  # Address ID
    AddressRowNumber = Column(Integer, nullable=True)  # Address row number
    AddressNote = Column(String, nullable=True)  # Address note
    AddressLine1 = Column(String, nullable=True)  # Address line 1
    AddressLine2 = Column(String, nullable=True)  # Address line 2
    AddressCity = Column(String, nullable=True)  # Address city
    AddressCountry = Column(String(10), nullable=True)  # Address country
    AddressPostalCode = Column(String, nullable=True)  # Address postal code
    AddressState = Column(String, nullable=True)  # Address state
    CurrencyID = Column(String(10), nullable=True)  # CurrencyID
    DateOfBirth = Column(DateTime, nullable=True)  # DateOfBirth
    DepartmentID = Column(String(30), nullable=True)  # DepartmentID
    EmployeeClassID = Column(String(10), nullable=True)  # EmployeeClassID
    EmployeeID = Column(String(30), nullable=True)  # EmployeeID
    EmploymentHistoryID = Column(String(36), nullable=True)  # EmploymentHistory ID
    EmploymentHistoryRowNumber = Column(Integer, nullable=True)  # EmploymentHistory row number
    EmploymentHistoryNote = Column(String, nullable=True)  # EmploymentHistory note
    EmploymentHistoryActive = Column(Boolean, nullable=True)  # EmploymentHistory active status
    EmploymentHistoryEndDate = Column(DateTime, nullable=True)  # EmploymentHistory end date
    EmploymentHistoryLineNbr = Column(Integer, nullable=True)  # EmploymentHistory line number
    EmploymentHistoryPositionID = Column(String(30), nullable=True)  # EmploymentHistory position ID
    EmploymentHistoryRehireEligible = Column(Boolean, nullable=True)  # EmploymentHistory rehire eligible
    EmploymentHistoryStartDate = Column(DateTime, nullable=True)  # EmploymentHistory start date
    EmploymentHistoryStartReason = Column(String, nullable=True)  # EmploymentHistory start reason
    EmploymentHistoryTerminated = Column(Boolean, nullable=True)  # EmploymentHistory terminated
    EmploymentHistoryTerminationReason = Column(String, nullable=True)  # EmploymentHistory termination reason
    ExpenseAccount = Column(String(30), nullable=True)  # ExpenseAccount
    ExpenseSubaccount = Column(String(30), nullable=True)  # ExpenseSubaccount
    IdentityNumber = Column(String(30), nullable=True)  # IdentityNumber
    IdentityType = Column(String(30), nullable=True)  # IdentityType
    LastModifiedDateTime = Column(DateTime, nullable=True)  # LastModifiedDateTime
    Name = Column(String, nullable=True)  # Name
    PaymentInstructionID = Column(String(36), nullable=True)  # PaymentInstruction ID
    PaymentInstructionRowNumber = Column(Integer, nullable=True)  # PaymentInstruction row number
    PaymentInstructionNote = Column(String, nullable=True)  # PaymentInstruction note
    PaymentInstructionBAccountID = Column(Integer, nullable=True)  # PaymentInstruction BAccountID
    PaymentInstructionDescription = Column(String, nullable=True)  # PaymentInstruction description
    PaymentInstructionInstructionID = Column(String(30), nullable=True)  # PaymentInstruction instruction ID
    PaymentInstructionLocationID = Column(Integer, nullable=True)  # PaymentInstruction location ID
    PaymentInstructionMethod = Column(String(10), nullable=True)  # PaymentInstruction method
    PaymentInstructionValue = Column(String, nullable=True)  # PaymentInstruction value
    PaymentMethod = Column(String(10), nullable=True)  # PaymentMethod
    ReportsToID = Column(String(30), nullable=True)  # ReportsToID
    SalesAccount = Column(String(30), nullable=True)  # SalesAccount
    SalesSubaccount = Column(String(30), nullable=True)  # SalesSubaccount
    Status = Column(String(30), nullable=True)  # Status
    Custom = Column(String, nullable=True)  # Store custom fields
    Links = Column(String, nullable=True)  # Store links as JSON

# Create the tables in the database
Base.metadata.create_all(bind=engine)
