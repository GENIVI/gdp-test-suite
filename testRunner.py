#!/usr/bin/python

# How to describe the tests/behaviours:
# * Define an scenario (one or two sentences)
# * Describe the acceptance test from the business and target perspective using the terminology: Given (set up) -> When (trigger) -> Then (verify) 
# * Description of the test as comments: Initial system state -> event (or action) -> Final system state & output -> Expected state & output 

# Scenario
# The user has shell access on image as root. Wayland is up and running and we want to test whether weston is also up and running.

# Acceptance test
# Test to confirm that  Weston is up and running
# Given that wayland was up and running
# When getting into the shell as root 
# And ask the system about weston
# Then 'active' is seen on the shell

# Technical description
# initial state - image is booted with an empty root password and an accessible ssh port from the host
# final state - the current state of the weston service is checked, 'active\n' should be returned

import geniviTest 
import unittest


class testRunner(geniviTest.TestGeniviQemu):
    # test must be called test_<testName>
    def test_rerecheckSystemCtl(self):
        # check weston is running (event)
        self.assertTrue(self.makeTest('systemctl is-active weston',
                                      'active\n')) # Final system state and output


if __name__ == '__main__': # Expected state & output, run test
    gensuite = unittest.TestLoader().loadTestsFromTestCase(testRunner)
    unittest.TextTestRunner(verbosity=2).run(gensuite)
