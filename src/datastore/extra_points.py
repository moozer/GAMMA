from datastore import Base
from sqlalchemy import Column, Integer, String
import collections


#class xxStudent( Base ):
#    __tablename__ = 'students'
#
#    id = Column(Integer, primary_key=True)
#    student_id = Column(String )
#    name = Column(String)

extra_points_record = collections.namedtuple( 'extra_points_record',
            [ 'date', 'student_id', 'points', "reason" ])
