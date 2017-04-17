from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

Base = declarative_base()

from student import *
from lesson import *
from lesson_points import *
from extra_points import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, asc

student_points_record = collections.namedtuple(
                            'student_points_record',
                            ['attendance', 'handins', 'absence', 'extra'])



class Datastore(object):
    def __init__(self, filename=":memory:"):
        engine = create_engine('sqlite:///%s' % filename, echo=False)

        # if not initialized...
        Base.metadata.create_all(engine)

        DatastoreSessionMaker = sessionmaker(bind=engine)
        self.session = DatastoreSessionMaker()

    # --- sql related decorators -----
    def db_guard(func):
        ''' handles commit on success and roolback om error
        '''
        def func_wrapper(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
                self.session.commit()
            except SQLAlchemyError:
                self.session.rollback()
                raise

        return func_wrapper

    # --- students ----
    @db_guard
    def add_student(self, student):
        u = Student(student_id=student.id,
                    name=student.name)

        self.session.add(u)

    def get_student(self, student_id):
        s = self.session.query(Student).filter(
                    Student.student_id == student_id
                    ).first()
        return student_record(s.student_id, "%s" % (s.name, ))

    def get_student_ids(self):
        ids = []
        for stud in self.session.query(
                            Student
                            ).order_by(asc(Student.student_id)):
            ids.append(stud.student_id)
        return ids

    def get_sum_by_student(self, student_id ):
       lesson_points_list = self.get_lesson_points_by_stud(student_id)
       extra_points_list = self.get_extra_points_by_student(student_id)

       return student_points_record(
            attendance=sum( 1 for entry in lesson_points_list if entry.attendance),
            handins=sum( 1 for entry in lesson_points_list if entry.handin),
            absence=sum( 1 for entry in lesson_points_list if entry.absence),
            extra=sum( ep.points for ep in extra_points_list ) )

    # --- lessons ----
    def get_lesson(self, id, id_type="Date"):
        return self.get_lesson_by_date(id)

    def get_lesson_by_date(self, lesson_date):
        s = self.session.query(Lesson).filter(
                    Lesson.date == lesson_date
                    ).first()
        return lesson_record(s.name, s.date)

    @db_guard
    def add_lesson(self, lesson):
        u = Lesson(date=lesson.date,
                    name=lesson.name)
        self.session.add(u)

    def get_lessons_list(self):
        return self.session.query(
                        Lesson.date,
                        Lesson.name
                        ).order_by(asc(Lesson.date))

    # --- lesson_points ----
    def add_lesson_points(self, lesson_points):
        sp = Lesson_points(lesson_id=lesson_points.lesson_id,
                            student_id=lesson_points.student_id,
                            attendance=lesson_points.attendance,
                            absence=lesson_points.absence,
                            handin=lesson_points.handin
                            )
        self.session.add(sp)
        self.session.commit()

    def get_lesson_points_by_lesson(self, lesson_id):
        sps = self.session.query(Lesson_points).filter(
                        Lesson_points.lesson_id == lesson_id)
        ret = []
        for sp in sps:
            ret.append(lesson_points_record(
                        sp.lesson_id, sp.student_id,
                        sp.attendance, sp.absence, sp.handin))
        return ret

    def get_lesson_points_by_stud(self, student_id):
        sps = self.session.query(Lesson_points).filter(
                        Lesson_points.student_id == student_id)
        ret = []
        for sp in sps:
            ret.append(lesson_points_record(
                         sp.lesson_id, sp.student_id,
                         sp.attendance, sp.absence, sp.handin))
        return ret

    # --- extra_points ----
    def add_extra_points(self, extra_points):
        sp = Extra_points(date=extra_points.date,
                          student_id=extra_points.student_id,
                          points=extra_points.points,
                          reason=extra_points.reason
                          )
        self.session.add(sp)
        self.session.commit()

    def get_extra_points_by_student(self, student_id):
        eps = self.session.query(Extra_points).filter(
                        Extra_points.student_id == student_id)
        ret = []
        for ep in eps:
            ret.append(extra_points_record(student_id=ep.student_id,
                                           date=ep.date,
                                           points=ep.points,
                                           reason=ep.reason))
        return ret
