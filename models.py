from sqlalchemy import Column, Integer, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    branch_id = Column(String, nullable=True)  # BranchID
    calendar = Column(String, nullable=True)  # Calendar
    cash_account = Column(String, nullable=True)  # CashAccount
    currency_id = Column(String, nullable=True)  # CurrencyID
    date_of_birth = Column(DateTime, nullable=True)  # DateOfBirth
    department_id = Column(String, nullable=True)  # DepartmentID
    employee_class_id = Column(String, nullable=True)  # EmployeeClassID
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

# Connection string
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
