#!/usr/bin/python
import sys
import unittest
import geniviTest 
# Allow the user to specify the tests to be run from the command line
# Assumes the script is run from that directory - doesn't use QEMU_SCRIPT_DIR

if __name__ == '__main__': # run all tests specified on command line
    loader = unittest.TestLoader()
    argv = sys.argv[1:]
    if argv == []:
        print 'no tests specified, supply names (w/out .py suffix)'
        sys.exit(1)
    suite = unittest.TestSuite()
    for arg in argv:
        suite.addTests(loader.loadTestsFromName(arg))

    testCount =  suite.countTestCases()
    if (testCount < 2):
        print 'running ', testCount, ' test'
    else:
        print 'running ', testCount, ' tests'

    if testCount > 0:
        geniviTest.TestGeniviQemu.poweron()
        unittest.TextTestRunner(verbosity=3).run(suite)
        geniviTest.TestGeniviQemu.poweroff()
