#!/usr/bin/python

# How to describe the tests/behaviours:
# * Define an scenario (one or two sentences)
# * Describe the acceptance test from the business and target perspective using the terminology: Given (set up) -> When (trigger) -> Then (verify) 
# * Description of the test as comments: Initial system state -> event (or action) -> Final system state & output -> Expected state & output 

# Scenario
# The user has shell access on image as root. We just want to check the connection.

# Acceptance test
# Get into the shell as root 

# Technical description
# initial state - image is booted with an empty root password and an accessible ssh port from the host
# final state - connecting via ssh to the image works

import geniviTest 
import unittest

class testSsh(geniviTest.TestGeniviQemu):
    # test must be called test_<testName>
    def test_ssh(self):
        # don't check the result if it runs on the board that is enough!
        ret = self.sendCommand(['echo', 'true'])

