from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from student import *
from session import *
from session_points import *
from extra_points import *

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


    # --- session_points ----
    def add_session_points( self, session_points ):
        sp = Session_points( session_id = session_points.session_id,
                            student_id  = session_points.student_id,
                            attendance  = session_points.attendance,
                            absence     = session_points.absence,
                            handin      = session_points.handin
                            )
        self.session.add( sp)
        self.session.commit()

    def get_session_points_by_session( self, session_id ):
        sps = self.session.query(Session_points).filter(Session_points.session_id==session_id)
        ret = []
        for sp in sps:
            ret.append( session_points_record( sp.session_id, sp.student_id,
                        sp.attendance, sp.absence, sp.handin))
        return ret

    def get_session_points_by_stud( self, student_id ):
        sps = self.session.query(Session_points).filter(Session_points.student_id==student_id)
        ret = []
        for sp in sps:
            ret.append( session_points_record( sp.session_id, sp.student_id,
                        sp.attendance, sp.absence, sp.handin))
        return ret

    # --- extra_points ----
    def add_extra_points( self, extra_points ):
        sp = Extra_points(   date        = extra_points.date,
                            student_id  = extra_points.student_id,
                            points      = extra_points.points,
                            reason     = extra_points.reason
                        )
        self.session.add( sp )
        self.session.commit()

    def get_extra_points_by_student( self, student_id ):
        eps = self.session.query(Extra_points).filter(Extra_points.student_id==student_id)
        ret = []
        for ep in eps:
            ret.append( extra_points_record( student_id = ep.student_id,
                                             date       = ep.date,
                                             points     = ep.points,
                                             reason     = ep.reason))
        return ret
