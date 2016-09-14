#!/usr/bin/python

# How to describe the tests/behavoiurs:
# * Define an scenario (one or two sentences)
# * Describe the acceptance test from the business and target perspective using the terminology: Given (set up) -> When (trigger) -> Then (verify) 
# * Description of the test as comments: Initial system state -> event (or action) -> Final system state & output -> Expected state & output 

# Scenario
# The user has shell access on image as root. Wayland is up and running and we want to ensure weston is also up and running.

# Acceptance test
# Test to confirm that  Weston is up and running
# Given that wayland was up and running
# And yy was up and runing
# When getting into the shell as root 
# And ask the system about weston
# Then sss is seen on the shell

# Technical description

import geniviTest 
import unittest

class testRunner(geniviTest.TestGeniviQemu):
    def test_rerecheckSystemCtl(self):
        # check weston is running (event)
        self.assertTrue(self.makeTest('systemctl is-active weston',
                                      'active\n')) # Final system state and output

if __name__ == '__main__': # Expected state & output, run test
    gensuite = unittest.TestLoader().loadTestsFromTestCase(testRunner)
    unittest.TextTestRunner(verbosity=2).run(gensuite)
