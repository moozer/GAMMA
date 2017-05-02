from datastore import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
import collections

from student import Student
from lesson import Lesson


class Lesson_points(Base):
	__tablename__ = 'lesson_points'

	id = Column(Integer, primary_key=True)
	lesson_id = Column(Date, ForeignKey("lessons.date"))
	student_id = Column(String, ForeignKey("students.student_id"))
	attendance = Column(Boolean)
	absence = Column(Boolean)
	handin = Column(Boolean)

lesson_points_record = collections.namedtuple(
		'lesson_points_record',
		['lesson_id', 'student_id', 'attendance', 'absence', 'handin'])
