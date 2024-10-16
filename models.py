from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_CONFIG = {
    "username": "sa",
    "password": "sa@121314",
    "host": "localhost",
    "port": "1433",
    "database": "MiHRS",
}

SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?driver=ODBC+Driver+17+for+SQL+Server"
)

# Creating the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# SQLAlchemy model for the employee table
class Employee(Base):
    __tablename__ = 'employee'

    id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    branch_id = Column(String, nullable=True)  # BranchID
    calendar = Column(String, nullable=True)  # Calendar
    cash_account = Column(String, nullable=True)  # CashAccount
    currency_id = Column(String, nullable=True)  # CurrencyID
    date_of_birth = Column(DateTime, nullable=True)  # DateOfBirth
    department_id = Column(String, nullable=True)  # DepartmentID
    employee_class_id = Column(String, nullable=True)  # EmployeeClassID
    employee_id = Column(String, nullable=True)  # EmployeeID
    expense_account = Column(String, nullable=True)  # ExpenseAccount
    expense_subaccount = Column(String, nullable=True)  # ExpenseSubaccount
    identity_number = Column(String, nullable=True)  # IdentityNumber
    identity_type = Column(String, nullable=True)  # IdentityType
    last_modified_date_time = Column(DateTime, nullable=True)  # LastModifiedDateTime
    name = Column(String, nullable=True)  # Name
    payment_method = Column(String, nullable=True)  # PaymentMethod
    reports_to_id = Column(String, nullable=True)  # ReportsToID
    sales_account = Column(String, nullable=True)  # SalesAccount
    sales_subaccount = Column(String, nullable=True)  # SalesSubaccount
    status = Column(String, nullable=True)  # Status
    custom_fields = Column(JSON, nullable=True)  # Store custom fields as JSON
    links = Column(JSON, nullable=True)  # Store links as JSON

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)
