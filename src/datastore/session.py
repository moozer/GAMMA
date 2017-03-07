from datastore import Base
from sqlalchemy import Column, Integer, String, Date
import collections


class Session( Base ):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    date = Column( Date )
    name = Column(String)

session_record = collections.namedtuple( 'session_record', ['name', 'date'])
