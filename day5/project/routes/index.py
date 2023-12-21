from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from day5.project.config.db import LocalSession, engine, Base
from day5.project.schema.index import EmployeeResponse, Token, TokenData, EmployeeCredential, EmployeeRequest, \
    ProjectRequest, ProjectResponse
from day5.project.service import service
from day5.project.exception.exception import EmployeeNotFoundException, EmployeeException
import logging
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

application = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

# JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MIN = os.getenv("ACCESS_TOKEN_EXPIRE_MIN")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


@application.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expire = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MIN))
    access_token = service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "Bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=401,
        detail="Could not validate"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_employee_by_email(email=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user: EmployeeRequest = Depends(get_current_user)):
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


@application.get("/employee", response_model=list[EmployeeResponse])
async def get_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        employees = service.get_employees(db, skip, limit)
        return employees
    except EmployeeException as e:
        logger.error(f"Error in get_employees route: {e.detail}")


@application.post("/employee", response_model=EmployeeResponse)
async def create_employee(emp: EmployeeRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating employee: {emp.name} ({emp.email}) with salary {emp.salary}")
        db_emp = service.create_employee(db, emp)
        logger.info(f"Employee created successfully: {db_emp.id}")
        return db_emp
    except EmployeeException as e:
        logger.error(f"Error in create_employee route: {e}")


@application.get("/employee/{emp_id}", response_model=EmployeeResponse)
async def get_employee(emp_id: int, db: Session = Depends(get_db)):
    try:
        employee = service.get_employee(db, emp_id)
        if not employee:
            raise EmployeeNotFoundException(emp_id=emp_id)
        return employee
    except Exception as e:
        logger.error(f"Error in get_employee route: {e}")
        raise EmployeeException(status_code=500, detail=e.__str__())


@application.delete("/employee/{emp_id}", response_model=EmployeeResponse)
async def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    try:
        employee = service.delete_employee(db, emp_id)
        if not employee:
            raise EmployeeNotFoundException(emp_id)
        return employee
    except Exception as e:
        logger.error(f"Error in delete_employee route: {e}")
        raise EmployeeException(status_code=500, detail=e.__str__())


@application.get("/employee", response_model=EmployeeResponse)
async def get_employee_by_email(email: EmailStr, db: Session = Depends(get_db)):
    try:
        employee = service.get_employee_by_email(db, email)
        if not employee:
            raise EmployeeNotFoundException(employee.id)
        return employee
    except Exception as e:
        logger.error(f"Error in get_employee_by_email route: {e}")
        raise EmployeeException(status_code=500, detail=e.__str__())


@application.post("/employee/{emp_id}/projects", response_model=ProjectResponse)
async def create_project_for_employee(emp_id: int, proj: ProjectRequest, db: Session = Depends(get_db)):
    try:
        employee = service.get_employee(db, emp_id)
        if not employee:
            raise EmployeeNotFoundException(emp_id)

        # Create the project
        created_project = service.create_project(db, proj, emp_id)
        return created_project
    except EmployeeException as e:
        logger.error(f"Employee Exception: {e.status_code} - {e.detail}")
    except Exception as e:
        logger.error(f"Error in create_project_for_employee route: {e}")
        raise EmployeeException(status_code=500, detail=e.__str__())


@application.get("/employee/{emp_id}/projects", response_model=list[ProjectResponse])
async def get_employee_projects(emp_id: int, db: Session = Depends(get_db)):
    try:
        projects = service.get_employee_projects(db, emp_id)
        return projects
    except Exception as e:
        logger.error(f"Error in get_employee_projects route: {e}")
        raise EmployeeException(status_code=500, detail=e.__str__())
