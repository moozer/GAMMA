from datastore import Base
from sqlalchemy import Column, Integer, String, Date
import collections


class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True)
    name = Column(String)

lesson_record = collections.namedtuple('lesson_record', ['name', 'date'])
