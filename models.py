from sqlalchemy import Column, Integer, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Address(Base):
    id = Column(String, nullable=True)
    rowNumber = Column(Integer, nullable=True)
    note = Column(String, nullable=True)
    AddressLine1 = Column(JSON, nullable=True)
    AddressLine2 = Column(JSON, nullable=True)
    City = Column(JSON, nullable=True)
    Country = Column(JSON, nullable=True)
    PostalCode = Column(JSON, nullable=True)
    State = Column(JSON, nullable=True)
    custom = Column(JSON, nullable=True)

class Contact(Base):
    id = Column(String, nullable=True)
    rowNumber = Column(Integer, nullable=True)
    note = Column(String, nullable=True)
    Activities = Column(JSON, nullable=True)
    Address = Column(Address, nullable=True)
    CurrencyID = Column(JSON, nullable=True)
    DateOfBirth = Column(JSON, nullable=True)
    DepartmentID = Column(JSON, nullable=True)
    EmployeeClassID = Column(JSON, nullable=True)
    EmployeeCost = Column(JSON, nullable=True)
    EmployeeID = Column(JSON, nullable=True)
    EmploymentHistory = Column(JSON, nullable=True)
    Name = Column(JSON, nullable=True)
    PaymentMethod = Column(JSON, nullable=True)
    ReportsToID = Column(JSON, nullable=True)
    Status = Column(JSON, nullable=True)
    custom = Column(JSON, nullable=True)

class CurrentEmployee(Base):
    AcctReferenceNbr = Column(JSON, nullable=True)
    UsrPlacementID = Column(JSON, nullable=True)
    CalendarID = Column(JSON, nullable=True)
    HoursValidation = Column(JSON, nullable=True)
    SalesPersonID = Column(JSON, nullable=True)
    UserID = Column(JSON, nullable=True)
    AllowOverrideCury = Column(JSON, nullable=True)
    CuryRateTypeID = Column(JSON, nullable=True)
    AllowOverrideRate = Column(JSON, nullable=True)
    LabourItemID = Column(JSON, nullable=True)
    UnionID = Column(JSON, nullable=True)
    RouteEmails = Column(JSON, nullable=True)
    TimeCardRequired = Column(JSON, nullable=True)
    NoteID = Column(JSON, nullable=True)
    PrepaymentAcctID = Column(JSON, nullable=True)
    PrepaymentSubID = Column(JSON, nullable=True)
    ExpenseAcctID = Column(JSON, nullable=True)
    ExpenseSubID = Column(JSON, nullable=True)
    SalesAcctID = Column(JSON, nullable=True)
    SalesSubID = Column(JSON, nullable=True)
    TermsID = Column(JSON, nullable=True)

class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
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

# Connection string
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
