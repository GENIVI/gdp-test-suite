#!/usr/bin/python

import unittest
import glob
import geniviTest 

class gdpTestSuite(unittest.TestSuite):
#    Testsuite
    def run(self, suite):
        geniviTest.TestGeniviQemu.poweron()
        super(gdpTestSuite,self).run(suite)
        geniviTest.TestGeniviQemu.poweroff()

# initialize the test suite
loader = unittest.TestLoader()
suite  = gdpTestSuite()

test_file_strings = glob.glob('test*.py')
modulenames = [str[0:len(str)-3] for str in test_file_strings]
# add tests to the test suite
for mod in modulenames:
    suite.addTests(loader.loadTestsFromName(mod))
suite.addTests(loader.loadTestsFromName('coreTests'))
               
gdprunner = unittest.TextTestRunner(verbosity=3)
gdprunner.run(suite)        
