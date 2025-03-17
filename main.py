from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
# from .models import Base , Employee
from os import getenv
from dotenv import load_dotenv

load_dotenv("./.env")

# Step 1: Initialize FastAPI app
app = FastAPI()

# Step 2: Configure PostgreSQL Database
DATABASE_URL = getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)  # Removed SQLite-specific connect_args
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Step 3: Define the Employee Model (Database Table)
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)   
    department = Column(String, index=True)
 

Base.metadata.create_all(engine)
# Alembic now handles creating the database schema. Remove Base.metadata.create_all(bind=engine)

# Step 4: CRUD Operations

# CREATE: Add a new employee
@app.post("/employees/")
def create_employee(name: str, email: str, department: str, db: Session = Depends(get_db)):
    new_employee = Employee(name=name, email=email, department=department)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# READ: Get all employees
@app.get("/employees/")
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

# READ: Get a single employee by ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# UPDATE: Update an employee's details
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, name: str = None, email: str = None, department: str = None, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if name:
        employee.name = name
    if email:
        employee.email = email
    if department:
        employee.department = department
    db.commit()
    db.refresh(employee)
    return employee

# DELETE: Delete an employee
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"detail": "Employee deleted successfully"}
