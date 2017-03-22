import unittest

import sys
sys.path.append( '..')

from datetime import date

from datastore.datastore import *


student_id = "abcd1234"
student_name = "John Doe"

test_year = 2017
test_month = 2
test_day = 3
some_date = date( test_year, test_month, test_day )
some_text = "awesome!"
lesson_name = "Some lesson"
lesson_date = some_date

class test_datastore_basic(unittest.TestCase):
    def testStudentMap(self):
        u = student_record( student_id, student_name)

        self.assertEqual( u.id, student_id )
        self.assertEqual( u.name, student_name )

    def testAddStudent( self ):
        u = student_record( student_id, student_name)
        ds = Datastore()

        ds.add_student( u )
        db_u = ds.get_student( student_id )

        self.assertEqual( u, db_u )

    def testLessonMap(self):
        s = lesson_record( lesson_name, lesson_date )

        self.assertEqual( s.name, lesson_name )
        self.assertEqual( s.date, lesson_date )

    def testAddLesson( self ):
        s = lesson_record( lesson_name, lesson_date )
        ds = Datastore()

        ds.add_lesson(s)
        db_s = ds.get_lesson( lesson_date )

        self.assertEqual( s, db_s )

    def testLessonPointsMap(self):
        s = lesson_points_record( lesson_date, student_id, True, False, True )

        self.assertEqual( s.student_id, student_id )
        self.assertEqual( s.lesson_id, lesson_date )
        self.assertEqual( s.attendance, True )
        self.assertEqual( s.absence, False )
        self.assertEqual( s.handin, True )

    def testAddLesson( self ):
        ses = lesson_record( lesson_name, lesson_date )
        stud = student_record( student_id, student_name)
        sp = lesson_points_record( lesson_date, student_id, True, False, True )

        ds = Datastore()

        ds.add_student( stud )
        ds.add_lesson( ses )
        ds.add_lesson_points( sp )

        db_ses = ds.get_lesson_points_by_lesson( lesson_date )
        self.assertEqual( sp, db_ses[0] )

        db_stud = ds.get_lesson_points_by_stud( student_id )
        self.assertEqual( sp, db_stud[0] )


    def testExtraPointsMap(self):
        ep = extra_points_record( some_date, student_id, points=5, reason=some_text )

        self.assertEqual( ep.student_id, student_id )
        self.assertEqual( ep.date, some_date )
        self.assertEqual( ep.points, 5 )
        self.assertEqual( ep.reason, some_text )

    def testAddExtraPoints( self ):
        ds = Datastore()

        stud = student_record( student_id, student_name)
        ds.add_student( stud )

        ep = extra_points_record( some_date, student_id, points=5, reason=some_text )
        ds.add_extra_points( ep )

        db_ses = ds.get_extra_points_by_student( student_id )
        self.assertEqual( ep, db_ses[0] )


class test_datastore_queries_Student(unittest.TestCase):
    def setUp( self ):
        self.ds = Datastore()
        for i in range( 0,10 ):
            u = student_record( 'john%04d'%(i, ), "John %d"%(i,) )
            self.ds.add_student( u )

    def testQueryStudent(self):
        for i in range( 0,10 ):
            u = self.ds.get_student( u'john%04d'%(i, ) )
            self.assertEqual( u.name, u"John %d"%(i,) )

    def testQueryStudentIds(self):
        ids = self.ds.get_student_ids()
        for i in range( 0,10 ):
            self.assertEqual( ids[i], u'john%04d'%(i, ) )

class test_datastore_queries_Lesson(unittest.TestCase):
    def setUp( self ):
        self.ds = Datastore()
        for i in range( 0,10 ):
            u = lesson_record( 'LearningLesson%04d'%(i, ), date( test_year, test_month, i+1 ) )
            self.ds.add_lesson( u )

    def testQueryLesson(self):
        for i in range( 0,10 ):
            u = self.ds.get_lesson( date( test_year, test_month, i+1 ) )
            self.assertEqual( u.name, 'LearningLesson%04d'%(i, ), )

    def testQueryLessons(self):
        lessons = self.ds.get_lessons_list()
        for i in range( 0,10 ):
            self.assertEqual( lessons[i][0], date( test_year, test_month, i+1 ) )


if __name__ == '__main__':
    unittest.main()
