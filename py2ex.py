#!/usr/bin/python

import unittest
from subprocess import call, Popen, check_output
import time
import os

arch='qemux86-64'



class TestGeniviQemu(unittest.TestCase):
    
    def sendCommand(self,cmd):
        op = check_output(cmd )
        return op
    
    def test_nestedCheckQemu(self):
        # looks for a qemux architecture in the dmesg output
        op = self.sendCommand(['dmesg']) #, '|', 'grep', 'qemux'])
        #print "<< " + op
        index = op.find('systemd[1]: Set hostname to <'+arch+'>.')
        self.assertTrue(index > 0)

    def test_checkNestedSystemCtl(self):
        # check weston is running
        op = self.sendCommand(['systemctl', 'is-active', 'weston'])
        # assumes Linux style EOLs
        self.assertEqual(op, 'active\n')

    

if __name__ == '__main__':
    # start the image

    gensuite = unittest.TestLoader().loadTestsFromTestCase(TestGeniviQemu)
    unittest.TextTestRunner(verbosity=2).run(gensuite)


    
