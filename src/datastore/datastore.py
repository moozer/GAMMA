from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Student( Base ):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    student_id = Column(String )
    name = Column(String)
