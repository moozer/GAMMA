from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from student import *
from session import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, asc

class Datastore( object ):
    def __init__( self, filename=":memory:" ):
        engine = create_engine('sqlite:///%s'%filename, echo=False)

        # if not initialized...
        Base.metadata.create_all(engine)

        DatastoreSessionMaker = sessionmaker(bind=engine)
        self.session = DatastoreSessionMaker()

    # --- students ----
    def add_student( self, student ):
        u = Student( student_id = student.id,
                     name = student.name)
        self.session.add( u)
        self.session.commit()

    def get_student( self, student_id ):
        s = self.session.query(Student).filter(Student.student_id==student_id).first()
        return student_record( s.student_id, "%s"%s.name)

    def get_student_ids( self ):
        ids = []
        for stud in self.session.query(Student).order_by(asc(Student.student_id)):
            ids.append( stud.student_id )
        return ids

    # --- sessions ----
    def get_session( self, id, id_type="Date"):
        return self.get_session_by_date( id )

    def get_session_by_date( self, session_date ):
        s = self.session.query(Session).filter(Session.date==session_date).first()
        return session_record( s.name, s.date )

    def add_session( self, session ):
        u = Session( date = session.date,
                     name = session.name)
        self.session.add( u)
        self.session.commit()

    def get_sessions_list( self ):
        return self.session.query(Session.date, Session.name).order_by(asc(Session.date))
