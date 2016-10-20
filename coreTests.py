#!/usr/bin/python

# These are some tests built up during the scoping out of the testing process
# They've been left as a single module containing multiple tests
import geniviTest 
import unittest
import os
import sys
from subprocess import call

class coreTests(geniviTest.TestGeniviQemu):


    # The following are sample tests
    def test_checkErrors(self):
        # tests for errors on startup, searching the output of dmesg for occurrences of the word error
        op = self.sendCommand(['dmesg',' |', 'grep', 'error', '|', 'wc', '-l'] )
        self.assertEqual(int(op),0)

    def test_checkFails(self):
        # tests for errors on startup, searching the output of dmesg for occurrences of the word failed
        op = self.sendCommand(['dmesg',' |', 'grep', '[Ff]ailed', '|', 'wc', '-l'] )
        # just the one failure:
        # acpi PNP0A03:00: _OSC failed (AE_NOT_FOUND); disabling ASPM
        #print '<', op, '>'
        self.assertEqual(int(op),1)

    def test_checkQemu(self):
        # looks for a qemux architecture in the dmesg output
        op = self.sendCommand(['dmesg', '-t', '|', 'grep', 'qemux'])
        self.assertEqual(op[0:-1],'systemd[1]: Set hostname to <'+self.arch+'>.') # trim EOL


    def test_checkPythonInstall(self):
        # op = self.sendCommand(['qml-example'])
        # qml-example can't yet fake a return (so not using anything gui related) instead copy a subset of these tests
        # onto the image and run then on the image locally
        # Not sure what this checks apart from the scp & the image having a working python installation!
        # needs a path prefix to py2ex.py
        scriptPath =  os.path.dirname(os.path.realpath(sys.argv[0]))
        call(['scp', '-o', 'StrictHostKeyChecking=no', '-P', self.port, scriptPath + '/py2ex.py', 'root@127.0.0.1:/tmp'])
        op = self.sendCommand(['/tmp/py2ex.py'])
        return True
    
    # this test seems to run last so no need for a restart??
    # and a test to timeout because it is shutdown?
    # A failure is expected because the image should be shutdown
    @unittest.expectedFailure
    def test_restart(self):
        self.sendCommand(["poweroff"])
        #time.sleep(2)
        # Assumes that it has worked without testing that?
        self.kvm = None
        op = self.sendCommand("uptime")
        self.assertEqual(op,"") # should have error'ed on the previous line
        self.pid = Popen(kvmCmd).pid
        

if __name__ == '__main__': # Expected state & output, run test
    gensuite = unittest.TestLoader().loadTestsFromTestCase(coreTests)
    unittest.TextTestRunner(verbosity=2).run(gensuite)
