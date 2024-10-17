from sqlalchemy import Column, String, Integer, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use a declarative base to define the database models
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'  # Table name

    id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    BranchID = Column(String(30), nullable=True)  # BranchID
    Calendar = Column(String(30), nullable=True)  # Calendar
    CashAccount = Column(String(30), nullable=True)  # CashAccount

    # Contact fields
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

    # Address fields
    AddressID = Column(String(36), nullable=True)  # Address ID
    AddressLine1 = Column(String, nullable=True)  # Address line 1
    AddressLine2 = Column(String, nullable=True)  # Address line 2
    AddressCity = Column(String, nullable=True)  # Address city
    AddressCountry = Column(String(10), nullable=True)  # Address country
    AddressPostalCode = Column(String, nullable=True)  # Address postal code
    AddressState = Column(String, nullable=True)  # Address state

    # Employee attributes
    CurrencyID = Column(String(10), nullable=True)  # CurrencyID
    DateOfBirth = Column(DateTime, nullable=True)  # DateOfBirth
    DepartmentID = Column(String(30), nullable=True)  # DepartmentID
    EmployeeClassID = Column(String(10), nullable=True)  # EmployeeClassID
    EmployeeID = Column(String(30), nullable=True)  # EmployeeID

    # Employment history fields
    EmploymentHistoryID = Column(String(36), nullable=True)  # EmploymentHistory ID
    EmploymentHistoryActive = Column(Boolean, nullable=True)  # EmploymentHistory active status
    EmploymentHistoryEndDate = Column(DateTime, nullable=True)  # EmploymentHistory end date
    EmploymentHistoryPositionID = Column(String(30), nullable=True)  # EmploymentHistory position ID
    EmploymentHistoryRehireEligible = Column(Boolean, nullable=True)  # EmploymentHistory rehire eligible
    EmploymentHistoryStartDate = Column(DateTime, nullable=True)  # EmploymentHistory start date
    EmploymentHistoryStartReason = Column(String, nullable=True)  # EmploymentHistory start reason
    EmploymentHistoryTerminated = Column(Boolean, nullable=True)  # EmploymentHistory terminated

    # Payment instruction fields
    PaymentInstructionID = Column(String(36), nullable=True)  # PaymentInstruction ID
    PaymentInstructionBAccountID = Column(Integer, nullable=True)  # PaymentInstruction BAccountID
    PaymentInstructionDescription = Column(String, nullable=True)  # PaymentInstruction description
    PaymentInstructionLocationID = Column(Integer, nullable=True)  # PaymentInstruction location ID
    PaymentMethod = Column(String(10), nullable=True)  # PaymentMethod
    Status = Column(String(30), nullable=True)  # Status

# SQLAlchemy connection string to your SQL Server
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/employee?driver=ODBC+Driver+17+for+SQL+Server"

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)
