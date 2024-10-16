from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(String(36), primary_key=True, index=True)  # Employee ID as the primary key
    row_number = Column(Integer, nullable=True)  # rowNumber
    note = Column(String, nullable=True)  # note field
    branch_id = Column(String(30), nullable=True)  # BranchID value
    calendar = Column(String(30), nullable=True)  # Calendar value
    cash_account = Column(String(30), nullable=True)  # CashAccount value
    currency_id = Column(String(10), nullable=True)  # CurrencyID value
    date_of_birth = Column(DateTime, nullable=True)  # DateOfBirth value
    department_id = Column(String(30), nullable=True)  # DepartmentID value
    employee_class_id = Column(String(10), nullable=True)  # EmployeeClassID value
    employee_id = Column(String(30), nullable=True)  # EmployeeID value
    name = Column(String(255), nullable=True)  # Name value
    payment_method = Column(String(10), nullable=True)  # PaymentMethod value
    status = Column(String(10), nullable=True)  # Status value
    expense_account = Column(String(30), nullable=True)  # ExpenseAccount value
    expense_subaccount = Column(String(30), nullable=True)  # ExpenseSubaccount value
    identity_number = Column(String(30), nullable=True)  # IdentityNumber value
    identity_type = Column(String(30), nullable=True)  # IdentityType value
    last_modified_date_time = Column(DateTime, nullable=True)  # LastModifiedDateTime value
    custom_fields = Column(JSON, nullable=True)  # Store custom fields as JSON
    links = Column(JSON, nullable=True)  # Store links as JSON

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(String(36), primary_key=True, index=True)
    employee_id = Column(String(36), nullable=False)  # Foreign key to Employee
    display_name = Column(String(255), nullable=True)  # DisplayName value
    email = Column(String(255), nullable=True)  # Email value
    phone1 = Column(String(50), nullable=True)  # Phone1 value
    phone1_type = Column(String(50), nullable=True)  # Phone1Type value
    phone2 = Column(String(50), nullable=True)  # Phone2 value
    phone2_type = Column(String(50), nullable=True)  # Phone2Type value
    title = Column(String(50), nullable=True)  # Title value
    custom = Column(JSON, nullable=True)  # Custom fields as JSON
    files = Column(JSON, nullable=True)  # Files as JSON

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(String(36), primary_key=True, index=True)
    contact_id = Column(String(36), nullable=False)  # Foreign key to Contact
    address_line1 = Column(String(255), nullable=True)  # AddressLine1 value
    address_line2 = Column(String(255), nullable=True)  # AddressLine2 value
    city = Column(String(255), nullable=True)  # City value
    country = Column(String(10), nullable=True)  # Country value
    postal_code = Column(String(10), nullable=True)  # PostalCode value
    state = Column(String(255), nullable=True)  # State value
    custom = Column(JSON, nullable=True)  # Custom fields as JSON
    files = Column(JSON, nullable=True)  # Files as JSON

class EmploymentHistory(Base):
    __tablename__ = 'employment_history'

    id = Column(String(36), primary_key=True, index=True)
    employee_id = Column(String(36), nullable=False)  # Foreign key to Employee
    active = Column(String(5), nullable=True)  # Active field
    start_date = Column(DateTime, nullable=True)  # StartDate value
    end_date = Column(DateTime, nullable=True)  # EndDate value
    position_id = Column(String(50), nullable=True)  # PositionID value
    rehire_eligible = Column(String(5), nullable=True)  # RehireEligible value
    start_reason = Column(String(50), nullable=True)  # StartReason value
    terminated = Column(String(5), nullable=True)  # Terminated value
    termination_reason = Column(String(255), nullable=True)  # TerminationReason value
    custom = Column(JSON, nullable=True)  # Custom fields as JSON
    links = Column(JSON, nullable=True)  # Links field
    files = Column(JSON, nullable=True)  # Files as JSON

class PaymentInstruction(Base):
    __tablename__ = 'payment_instructions'

    id = Column(String(36), primary_key=True, index=True)
    employee_id = Column(String(36), nullable=False)  # Foreign key to Employee
    b_account_id = Column(String(30), nullable=True)  # BAccountID value
    description = Column(String(255), nullable=True)  # Description value
    instruction_id = Column(String(10), nullable=True)  # InstructionID value
    location_id = Column(String(10), nullable=True)  # LocationID value
    payment_method = Column(String(30), nullable=True)  # PaymentMethod value
    value = Column(String(255), nullable=True)  # Value field
    custom = Column(JSON, nullable=True)  # Custom fields as JSON
    files = Column(JSON, nullable=True)  # Files as JSON

# Database connection settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa@121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
