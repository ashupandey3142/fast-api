from day5.project.config.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), index=True)
    email = Column(String(60), index=True)
    hash_password = Column(String(60))
    salary = Column(Integer, index=True)

    projects = relationship("Project", back_populates="developer")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60), index=True)
    description = Column(String(100), index=True)
    developer_id = Column(Integer, ForeignKey("employee.id"))

    developer = relationship("Employee", back_populates="projects")
