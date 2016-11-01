#!/usr/bin/python

#
# Assumptions
# Script is run in directory containing scripts -  see QEMU_IMAGE_DIR
# for specifying the image location.
# See QEMU_SCRIPT_DIR for specifying the scripts location (coreTests is always found)
#
# Python modules unittest, time, glob, sys, os
#
import unittest
import glob
import geniviTest 
import sys
import os

class gdpTestSuite(unittest.TestSuite):
#    a TestSuite, override run to handle starting and closing the image
    def run(self, suite):
        geniviTest.TestGeniviQemu.poweron()
        super(gdpTestSuite,self).run(suite)
        geniviTest.TestGeniviQemu.poweroff()

# initialize the test suite
loader = unittest.TestLoader()
suite  = gdpTestSuite()

# assumes script is run in the directory containing the tests
# no it doesn't!
if  (os.environ.has_key('QEMU_SCRIPT_DIR')):
    scriptDir = os.environ['QEMU_SCRIPT_DIR']
else:    
    scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))

sys.path.append(scriptDir)
sys.path.append(scriptDir+'/unitTests')
    
test_file_strings = glob.glob(scriptDir + '/unitTests/test*.py')

# Having found the scripts using globbing remove the full path and the .py suffix
modulenames = [str[str.rfind('/')+1:len(str)-3] for str in test_file_strings]
# add tests to the test suite
for mod in modulenames:
    suite.addTests(loader.loadTestsFromName(mod))

# add base tests always
suite.addTests(loader.loadTestsFromName('coreTests'))
               
gdprunner = unittest.TextTestRunner(verbosity=3)
gdprunner.run(suite)        
