from pydantic import BaseModel, EmailStr


class ProjectBase(BaseModel):
    title: str
    description: str


class ProjectRequest(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    developer_id: int

    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    disable: bool = False
    salary: int


class EmployeeRequest(EmployeeBase):
    password: str


class EmployeeResponse(EmployeeBase):
    id: int
    projects: list[ProjectResponse] = []

    class Config:
        orm_mode = True


class EmployeeCredential(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
