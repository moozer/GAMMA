from datastore import Base
from sqlalchemy import Column, Integer, String, Date, Boolean
import collections


class Session_points( Base ):
    __tablename__ = 'session_pointss'

    id = Column(Integer, primary_key=True)
    session_id = Column( Date )
    student_id = Column(String)
    attendance = Column( Boolean )
    absence = Column( Boolean )
    handin = Column( Boolean )

session_points_record = collections.namedtuple(
        'session_points_record',
        ['session_id', 'student_id', 'attendance', 'absence', 'handin'])
