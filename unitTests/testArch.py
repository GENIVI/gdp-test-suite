#!/usr/bin/python

# How to describe the tests/behaviours:
# * Define an scenario (one or two sentences)
# * Describe the acceptance test from the business and target perspective using the terminology: Given (set up) -> When (trigger) -> Then (verify) 
# * Description of the test as comments: Initial system state -> event (or action) -> Final system state & output -> Expected state & output 

# Scenario
# The user has shell access on image as root. We want to test that the image is a QEMU build

# Acceptance test
# Test to confirm that dmesg confirms that this is a qemux86-64 build
# When getting into the shell as root 
# And ask the system about the kernel ring buffer
# Then setting the hostname to qemux86-64 is shown in the otput

# Technical description
# initial state - image is booted with an empty root password and an accessible ssh port from the host
# final state - the current state of the hostname is checked, 'qemux86-64' should be returned

# Maybe we should just check hostname?

import geniviTest 
import unittest

class testRunner(geniviTest.TestGeniviQemu):
    def test_checkQemu(self):
        # looks for a qemux architecture in the dmesg output
        op = self.sendCommand(['dmesg', '-t', '|', 'grep', 'qemux'])
        self.assertEqual(op[0:-1],'systemd[1]: Set hostname to <'+self.arch+'>.')
