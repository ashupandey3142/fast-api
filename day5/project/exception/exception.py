from fastapi import HTTPException


class EmployeeNotFoundException(HTTPException):
    def __init__(self, emp_id: int):
        detail = f"Employee with ID {emp_id} not found"
        super().__init__(status_code=404, detail=detail)


class EmployeeException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
