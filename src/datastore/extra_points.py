from datastore import Base
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint, ForeignKey
import collections


class Extra_points(Base):
    __tablename__ = 'extra_points'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    student_id = Column(String, ForeignKey("students.student_id") )
    points = Column(Integer)
    reason = Column(String)
    __table_args__ = (UniqueConstraint('date', 'student_id', 'reason', name='no_dupes'),
                     )
extra_points_record = collections.namedtuple(
            'extra_points_record',
            ['date', 'student_id', 'points', "reason"])
