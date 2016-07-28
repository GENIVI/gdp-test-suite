#!/usr/bin/python
import unittest
from subprocess import call, Popen, check_output
import time

baseSsh = ['ssh', '-o', 'StrictHostKeyChecking=no', 'root@127.0.0.1', '-p', '5555']

def setUpModule():
    pid = Popen(['/bin/sh', '-c', '~/bin/qemu-gdp']).pid
    #call(["qemu-gdp", "&"]) # should we build the kvm command here?
    time.sleep(7) # semi random number!

def tearDownModule():
    call(baseSsh + ["poweroff"])

class TestGeniviQemu(unittest.TestCase):
    
    def test_checkErrors(self):
        # tests for errors on startup
        op = check_output(baseSsh + ['dmesg',' |', 'grep', 'error', '|', 'wc', '-l'] )
        self.assertEqual(int(op),0)
    def test_checkQemu(self):
        # looks for a qemu architecture in the dmesg output
        op = check_output(baseSsh + ['dmesg',' |', 'grep', 'qemux' , '|', 'wc', '-w'])
        self.assertEqual(int(op),7) #'Set hostname to <qemux86>.') # trim prefix
    def test_checkSystemCtl(self):
        # checks the number of active system services (is this too prescriptive?
        op = check_output(baseSsh + ['systemctl', '|', 'grep', 'active', '|', 'grep', 'inactive']) #, '|', 'grep', '362'])
        #print "<", op, ">" hmm is it really const?
        self.assertEqual(int(op.split(None, 1)[0]), 362)
        # '362 loaded units listed. Pass --all to see loaded but inactive units, too.')
    # and a test to timeout because it is shutdown
    

if __name__ == '__main__':
    # start the image

    gensuite = unittest.TestLoader().loadTestsFromTestCase(TestGeniviQemu)
    unittest.TextTestRunner(verbosity=2).run(gensuite)

#    call(baseSsh + ["poweroff"])

    
