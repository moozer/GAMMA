from datastore import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
import collections

from student import Student
from session import Session


class Session_points(Base):
    __tablename__ = 'session_points'

    id = Column(Integer, primary_key=True)
    session_id = Column(Date, ForeignKey("sessions.date"))
    student_id = Column(String, ForeignKey("students.student_id"))
    attendance = Column(Boolean)
    absence = Column(Boolean)
    handin = Column(Boolean)

session_points_record = collections.namedtuple(
        'session_points_record',
        ['session_id', 'student_id', 'attendance', 'absence', 'handin'])
