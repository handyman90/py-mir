from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'  # Update this to your actual table name

    id = Column(String(36), primary_key=True, index=True)
    row_number = Column(Integer, nullable=True)
    note = Column(String, nullable=True)
    branch_id = Column(String(30), nullable=True)
    calendar = Column(String(30), nullable=True)
    cash_account = Column(String(30), nullable=True)
    currency_id = Column(String(10), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    department_id = Column(String(30), nullable=True)
    employee_class_id = Column(String(10), nullable=True)
    employee_id = Column(String(30), nullable=True)
    name = Column(String(255), nullable=True)
    payment_method = Column(String(10), nullable=True)
    status = Column(String(10), nullable=True)
    custom_fields = Column(JSON, nullable=True)
    links = Column(JSON, nullable=True)

# Database connection settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa@121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
