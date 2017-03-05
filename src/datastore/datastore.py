from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from student import *
from sqlalchemy.orm import sessionmaker


class Datastore( object ):
    def __init__( self, filename=":memory:" ):
        engine = create_engine('sqlite:///%s'%filename, echo=False)

        # if not initialized...
        Base.metadata.create_all(engine)

        DatastoreSessionMaker = sessionmaker(bind=engine)
        self.session = DatastoreSessionMaker()

    def add_student( self, student_id, student_name ):
        u = Student( student_id = student_id, name=student_name)
        self.session.add( u)
        self.session.commit()

    def get_student( self, student_id ):
        s = self.session.query(Student).filter(Student.student_id==student_id).first()
        return student_record( s.student_id, "%s"%s.name)
