from datastore import Base
from sqlalchemy import Column, Integer, String, Date
import collections


class Extra_points(Base):
	__tablename__ = 'extra_points'

	id = Column(Integer, primary_key=True)
	date = Column(Date)
	student_id = Column(String)
	points = Column(Integer)
	reason = Column(String)

extra_points_record = collections.namedtuple(
			'extra_points_record',
			['date', 'student_id', 'points', "reason"])
