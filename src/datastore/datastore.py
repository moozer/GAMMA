from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=False)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

class Student( Base ):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    student_id = Column(String )
    name = Column(String)

Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
