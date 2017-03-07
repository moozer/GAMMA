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

    def testAddStudent( self ):
        u = student_record( student_id, student_name)
        ds = Datastore()

        ds.add_student( u )
        db_u = ds.get_student( student_id )

        self.assertEqual( u, db_u )


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



if __name__ == '__main__':
    unittest.main()
