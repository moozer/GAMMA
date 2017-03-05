import unittest

import sys
sys.path.append( '..')

from datastore.datastore import *

student_id = "abcd1234"
student_name = "John Doe"

class test_datastore_basic_Student(unittest.TestCase):
    def testStudentMap(self):
        u = student_record( student_id, student_name)

        self.assertEqual( u.id, student_id )
        self.assertEqual( u.name, student_name )

    # def testAddStudent( self ):
    #     u = Student( student_id = student_id, name=student_name)
    #
    #
    #     test_session = Session()
    #     test_session.add( u)
    #     test_session.commit()
    #
    #     rowcount = test_session.query(Student).count()
    #
    #     self.assertEqual(rowcount, 1 )
    #     self.assertTrue( u.id)

class test_datastore_queries_Student(unittest.TestCase):
    def setUp( self ):
        self.ds = Datastore()
        for i in range( 0,10 ):
            self.ds.add_student( student_id = 'john%04d'%(i, ), student_name="John %d"%(i,) )

    def testQueryStudent(self):
        for i in range( 0,10 ):
            u = self.ds.get_student( u'john%04d'%(i, ) )
            self.assertEqual( u.name, u"John %d"%(i,) )

    def testQueryStudentIds(self):
        ids = self.ds.get_student_ids()
        for i in range( 0,10 ):
            self.assertEqual( ids[i], u'john%04d'%(i, ) )



if __name__ == '__main__':
    unittest.main()
