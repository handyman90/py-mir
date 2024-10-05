from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(String(36), primary_key=True, index=True)  # employee_id as the primary key
    row_number = Column(Integer, nullable=True)
    note = Column(String, nullable=True)
    branch_id = Column(String, nullable=True)
    contact_id = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_first_name = Column(String, nullable=True)
    contact_last_name = Column(String, nullable=True)
    contact_phone1 = Column(String, nullable=True)
    contact_phone2 = Column(String, nullable=True)
    contact_title = Column(String, nullable=True)
    currency_id = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    department_id = Column(String, nullable=True)
    employee_class_id = Column(String, nullable=True)
    employee_cost = Column(JSON, nullable=True)
    employment_history = Column(JSON, nullable=True)
    status = Column(String, nullable=True)
    custom_fields = Column(JSON, nullable=True)

# Connection string
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa%40121314@localhost:1433/MiHRS?driver=ODBC+Driver+17+for+SQL+Server"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
