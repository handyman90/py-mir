from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Database configuration with your password
SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"
)

# Creating the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# SQLAlchemy model for the Address table
class Address(Base):
    __tablename__ = 'address'
    
    id = Column(String(36), primary_key=True, index=True)  # Address ID
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    address_line1 = Column(String, nullable=True)  # AddressLine1
    address_line2 = Column(String, nullable=True)  # AddressLine2
    city = Column(String, nullable=True)  # City
    country = Column(String, nullable=True)  # Country
    postal_code = Column(String, nullable=True)  # PostalCode
    state = Column(String, nullable=True)  # State

# SQLAlchemy model for the Contact table
class Contact(Base):
    __tablename__ = 'contact'
    
    id = Column(String(36), primary_key=True, index=True)  # Contact ID
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    display_name = Column(String, nullable=True)  # DisplayName
    email = Column(String, nullable=True)  # Email
    fax = Column(String, nullable=True)  # Fax
    first_name = Column(String, nullable=True)  # FirstName
    last_name = Column(String, nullable=True)  # LastName
    middle_name = Column(String, nullable=True)  # MiddleName
    phone1 = Column(String, nullable=True)  # Phone1
    phone1_type = Column(String, nullable=True)  # Phone1Type
    phone2 = Column(String, nullable=True)  # Phone2
    phone2_type = Column(String, nullable=True)  # Phone2Type
    title = Column(String, nullable=True)  # Title
    address_id = Column(String, ForeignKey('address.id'), nullable=True)  # Foreign Key to Address

    # Relationship
    address = relationship("Address", back_populates="contacts")

# SQLAlchemy model for the EmploymentHistory table
class EmploymentHistory(Base):
    __tablename__ = 'employment_history'
    
    id = Column(String(36), primary_key=True, index=True)  # Employment History ID
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    active = Column(String, nullable=True)  # Active
    end_date = Column(DateTime, nullable=True)  # EndDate
    line_nbr = Column(Integer, nullable=True)  # LineNbr
    position_id = Column(String, nullable=True)  # PositionID
    rehire_eligible = Column(String, nullable=True)  # RehireEligible
    start_date = Column(DateTime, nullable=True)  # StartDate
    start_reason = Column(String, nullable=True)  # StartReason
    terminated = Column(String, nullable=True)  # Terminated
    termination_reason = Column(String, nullable=True)  # TerminationReason

# SQLAlchemy model for the PaymentInstruction table
class PaymentInstruction(Base):
    __tablename__ = 'payment_instruction'
    
    id = Column(String(36), primary_key=True, index=True)  # Payment Instruction ID
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    b_account_id = Column(Integer, nullable=True)  # BAccountID
    description = Column(String, nullable=True)  # Description
    instruction_id = Column(String, nullable=True)  # InstructionID
    location_id = Column(Integer, nullable=True)  # LocationID
    payment_method = Column(String, nullable=True)  # PaymentMethod
    value = Column(String, nullable=True)  # Value

# SQLAlchemy model for the employee table
class Employee(Base):
    __tablename__ = 'employee'

    id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    branch_id = Column(String(30), nullable=True)  # BranchID
    calendar = Column(String(30), nullable=True)  # Calendar
    cash_account = Column(String(30), nullable=True)  # CashAccount
    currency_id = Column(String(10), nullable=True)  # CurrencyID
    date_of_birth = Column(DateTime, nullable=True)  # DateOfBirth
    department_id = Column(String(30), nullable=True)  # DepartmentID
    employee_class_id = Column(String(10), nullable=True)  # EmployeeClassID
    employee_id = Column(String(30), nullable=True)  # EmployeeID
    expense_account = Column(String(30), nullable=True)  # ExpenseAccount
    expense_subaccount = Column(String(30), nullable=True)  # ExpenseSubaccount
    identity_number = Column(String(30), nullable=True)  # IdentityNumber
    identity_type = Column(String(30), nullable=True)  # IdentityType
    last_modified_date_time = Column(DateTime, nullable=True)  # LastModifiedDateTime
    name = Column(String(255), nullable=True)  # Name
    payment_method = Column(String(10), nullable=True)  # PaymentMethod
    reports_to_id = Column(String, nullable=True)  # ReportsToID
    sales_account = Column(String(30), nullable=True)  # SalesAccount
    sales_subaccount = Column(String(30), nullable=True)  # SalesSubaccount
    status = Column(String, nullable=True)  # Status

    # Relationships
    contact = relationship("Contact", back_populates="employee", uselist=False)
    employment_history = relationship("EmploymentHistory", back_populates="employee")
    payment_instruction = relationship("PaymentInstruction", back_populates="employee")

# Create all tables in the database (if they don't already exist)
Base.metadata.create_all(bind=engine)
