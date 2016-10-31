#!/usr/bin/python
from __future__ import print_function
import sys
import os
import unittest
import geniviTest

# Allow the user to specify the tests to be run from the command line
# Assumes the script is run from the gdp-src-build directory - it doesn't use QEMU_SCRIPT_DIR

if __name__ == '__main__': # run all tests specified on command line
    scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))

    sys.path.append(scriptDir+'/unitTests')
    loader = unittest.TestLoader()
    argv = sys.argv[1:]
    if argv == []:
        print ('no tests specified, supply names (w/out .py suffix)')
        sys.exit(1)
    suite = unittest.TestSuite()
    for arg in argv:
        try:
            suite.addTests(loader.loadTestsFromName(arg))
        except ImportError:
            print ('*** test', arg, 'not found')
            pass
    testCount =  suite.countTestCases()
    print ('running', testCount, 'test', end="")
    if (testCount != 1):
        print("s")
    else:
        print ("")
    if testCount > 0:
        geniviTest.TestGeniviQemu.poweron()
        unittest.TextTestRunner(verbosity=3).run(suite)
        geniviTest.TestGeniviQemu.poweroff()
