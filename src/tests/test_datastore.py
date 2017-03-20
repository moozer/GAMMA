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
session_name = "Some session"
session_date = some_date

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

    def testSessionMap(self):
        s = session_record( session_name, session_date )

        self.assertEqual( s.name, session_name )
        self.assertEqual( s.date, session_date )

    def testAddSession( self ):
        s = session_record( session_name, session_date )
        ds = Datastore()

        ds.add_session(s)
        db_s = ds.get_session( session_date )

        self.assertEqual( s, db_s )

    def testSessionPointsMap(self):
        s = session_points_record( session_date, student_id, True, False, True )

        self.assertEqual( s.student_id, student_id )
        self.assertEqual( s.session_id, session_date )
        self.assertEqual( s.attendance, True )
        self.assertEqual( s.absence, False )
        self.assertEqual( s.handin, True )

    def testAddSession( self ):
        ses = session_record( session_name, session_date )
        stud = student_record( student_id, student_name)
        sp = session_points_record( session_date, student_id, True, False, True )

        ds = Datastore()

        ds.add_student( stud )
        ds.add_session( ses )
        ds.add_session_points( sp )

        db_ses = ds.get_session_points_by_session( session_date )
        self.assertEqual( sp, db_ses[0] )

        db_stud = ds.get_session_points_by_stud( student_id )
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

class test_datastore_queries_Session(unittest.TestCase):
    def setUp( self ):
        self.ds = Datastore()
        for i in range( 0,10 ):
            u = session_record( 'LearningSession%04d'%(i, ), date( test_year, test_month, i+1 ) )
            self.ds.add_session( u )

    def testQuerySession(self):
        for i in range( 0,10 ):
            u = self.ds.get_session( date( test_year, test_month, i+1 ) )
            self.assertEqual( u.name, 'LearningSession%04d'%(i, ), )

    def testQuerySessions(self):
        sessions = self.ds.get_sessions_list()
        for i in range( 0,10 ):
            self.assertEqual( sessions[i][0], date( test_year, test_month, i+1 ) )


if __name__ == '__main__':
    unittest.main()
