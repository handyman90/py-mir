from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    status = Column(String)

    # Contact Info
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone1 = Column(String, nullable=True)
    phone2 = Column(String, nullable=True)
    phone3 = Column(String, nullable=True)
    fax = Column(String, nullable=True)
    identity_number = Column(String)
    identity_type = Column(String)
    title = Column(String)

    # Employment History
    position_id = Column(String)
    start_date = Column(DateTime)
    start_reason = Column(String)
    end_date = Column(DateTime, nullable=True)
    active = Column(Boolean)
    rehire_eligible = Column(Boolean)
    termination_reason = Column(String, nullable=True)

    # Employee Settings
    branch_id = Column(String)
    department_id = Column(String)
    employee_class = Column(String)
    
    # Financial Settings
    ap_account = Column(String, nullable=True)
    ap_subaccount = Column(String, nullable=True)
    expense_account = Column(String, nullable=True)
    expense_subaccount = Column(String, nullable=True)
    sales_account = Column(String, nullable=True)
    sales_subaccount = Column(String, nullable=True)

# Set up the database connection (replace credentials as needed)
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://username:password@server/dbname?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
