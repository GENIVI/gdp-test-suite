#!/usr/bin/python

import geniviTest 
import unittest

class testRunner(geniviTest.TestGeniviQemu):
    def test_rerecheckSystemCtl(self):
        # check weston is running
        self.assertTrue(self.makeTest('systemctl is-active weston', 'active\n'))

if __name__ == '__main__':
    gensuite = unittest.TestLoader().loadTestsFromTestCase(testRunner)
    unittest.TextTestRunner(verbosity=2).run(gensuite)
