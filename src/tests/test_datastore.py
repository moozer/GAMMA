import unittest

import sys
sys.path.append( '..')

from datastore.datastore import *

student_id = "abcd1234"
student_name = "John Doe"

class test_datastore(unittest.TestCase):
    def testStudentMap(self):
        u = Student( student_id = student_id, name=student_name)

        self.assertEqual( u.student_id, student_id )
        self.assertEqual( u.name, student_name )

    def testAddStudent( self ):
        u = Student( student_id = student_id, name=student_name)

        test_session = Session()
        test_session.add( u)
        test_session.commit()

        self.assertTrue( u.id)

if __name__ == '__main__':
    unittest.main()
