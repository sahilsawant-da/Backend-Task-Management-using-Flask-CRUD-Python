from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , Enum
from sqlmodel import SQLModel , Field , Session , select
from typing import optional 
Base = declarative_base()
from uuid import UUID , uuid4

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String, index=True)


class EmployeeBase(SQLModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1 , unique=True, nullable=False)
    department: optional[str] = Field (min_length=1)

class employeecreate(EmployeeBase):
        pass

class employeeread(EmployeeBase):
       id: UUID


class Employee(EmployeeBase, table=True):  # The table model
      id: UUID = Field(default_factory=uuid4, primary_key=True)