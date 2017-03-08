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
session_name = "Some session"
session_date = date( test_year, test_month, test_day )

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
