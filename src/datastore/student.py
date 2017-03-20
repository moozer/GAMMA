from datastore import Base
from sqlalchemy import Column, Integer, String
import collections


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    student_id = Column(String)
    name = Column(String)

student_record = collections.namedtuple('student_record', ['id', 'name'])
