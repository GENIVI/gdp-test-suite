#!/usr/bin/python

# How to describe the tests/behaviours:
# * Define an scenario (one or two sentences)
# * Describe the acceptance test from the business and target perspective using the terminology: Given (set up) -> When (trigger) -> Then (verify) 
# * Description of the test as comments: Initial system state -> event (or action) -> Final system state & output -> Expected state & output 

# Scenario
# The user has shell access on image as root. We want to check the number of running services

# Acceptance test
# Test to confirm that 362 services are running
# Given that wayland was up and running
# When getting into the shell as root 
# And ask systemctl about the active services
# The final grep inactive is to pull out the summary line

# Technical description
# initial state - image is booted with an empty root password and an accessible ssh port from the host
# final state - summary of running services is returned by sendCommand, the assertEqual checks that the
#               count if 362 (full result should be '362 loaded units listed. Pass --all to see loaded but inactive units, too.')


import geniviTest 
import unittest
 
class testServices(geniviTest.TestGeniviQemu):
    # test must be called test_<testName>
    def test_checkSystemCtlActive(self):
        # checks the number of active system services (is this too prescriptive?
        op = self.sendCommand(['systemctl', '|', 'grep', 'active', '|', 'grep', 'inactive'])
        self.assertEqual(int(op.split(None, 1)[0]), 362)
        # '362 loaded units listed. Pass --all to see loaded but inactive units, too.')


