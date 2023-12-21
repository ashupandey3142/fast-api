from datetime import timedelta, datetime
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from day5.project.models.index import Employee, Project
from day5.project.schema.index import EmployeeRequest, ProjectRequest
from day5.project.utils.util import convert_hash, verify_password
from pydantic import EmailStr
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, username: EmailStr, password: str):
    user = db.query(Employee).filter(Employee.email == username).first()
    print(username)
    print(user)
    if not user:
        return False
    if not verify_password(password, hashed_password=user.hash_password):
        return False
    return user


def get_employee(db: Session, emp_id: int):
    return db.query(Employee).filter(Employee.id == emp_id)


def get_employee_by_email(db: Session, email: EmailStr):
    return db.query(Employee).filter(Employee.email == email)


def create_employee(db: Session, emp: EmployeeRequest):
    hash_pass = convert_hash(emp.password)
    db_emp = Employee(name=emp.name, hash_password=hash_pass, email=emp.email, salary=emp.salary)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


def delete_employee(db: Session, emp_id: int):
    emp = db.query(Employee).filter(Employee.id == emp_id)
    db.delete(emp)
    db.commit()
    db.refresh(emp)
    return emp


def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id)


def create_project(db: Session, proj: ProjectRequest, emp_id):
    db_proj = Project(**proj.model_dump(), developer_id=emp_id)
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj


def get_employee_projects(db: Session, emp_id: int):
    return db.query(Project).filter(Project.developer_id == emp_id).all()
