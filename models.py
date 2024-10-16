from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'  # Change this to your actual table name

    employee_id = Column(String(36), primary_key=True, index=True)  # UUID or unique identifier
    row_number = Column(Integer, nullable=True)  # Corresponds to rowNumber
    note = Column(String, nullable=True)  # Note field
    branch_id = Column(String, nullable=True)  # BranchID
    currency_id = Column(String, nullable=True)  # CurrencyID
    date_of_birth = Column(DateTime, nullable=True)  # DateOfBirth
    department_id = Column(String, nullable=True)  # DepartmentID
    employee_class_id = Column(String, nullable=True)  # EmployeeClassID
    name = Column(String, nullable=True)  # Name
    payment_method = Column(String, nullable=True)  # PaymentMethod
    status = Column(String, nullable=True)  # Status
    custom_fields = Column(JSON, nullable=True)  # Store custom fields as JSON

# Database connection settings (update these as needed)
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Create a new SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
