#!/usr/bin/python
import unittest
from subprocess import call, Popen, check_output
import time
import os
import sys
#
# Assumptions
# Script is run in gdp-src-build - though see QEMU_IMAGE_DIR
# Python modules unittest, time
#

#
# Assumptions
# Script is run in gdp-src-build
# Python modules unittest, time
#

# variables which might need changing
arch='qemux86-64'
fs='genivi-dev-platform-'+arch+'.ext4'
image='bzImage'
port = '5555'
sleepBeforeTime = 6 # time to sleep to allow vm to start, too short and it may fail, make it long enough
                    # to try to align the vm and the tests, also if short the ssh may wait to retry making
                    # the test time longer!
# end of configurable area

# the user can set the environment varible QEMU_IMAGE_DIR to determine
# the directory containing the kernel/disk image
if  (os.environ.has_key('QEMU_IMAGE_DIR')):
    dir = os.environ['QEMU_IMAGE_DIR'] + '/'
else:
    dir='tmp/deploy/images/'+arch+'/'
if not os.path.isfile(dir+image) :
    print fs
    raise Exception("Image file not found - do you need to set QEMU_IMAGE_DIR?")

# Assumes that the image has been built with EXTRA_USERS_PARAMS = ""
# If it hasn't you may need to install sshpass and edit the parameters!
baseSsh = ['ssh', '-o', 'StrictHostKeyChecking=no', 'root@127.0.0.1', '-p', port, '-o', 'ConnectTimeout=7',
           '-o', 'BatchMode=yes']

kvmCmd = [
          'kvm', '-kernel', dir+image, '-net', 'nic',
          '-net', 'user,hostfwd=tcp::'+port+'-:22', # open port 5555 for ssh access
          '-cpu', 'core2duo',
          '-hda', dir+fs, 
          '-vga', 'std',  '-no-reboot', '-m', '512',
          '--append', 'vga=0 uvesafb.mode_option=640x480-32 root=/dev/hda rw mem=512M  oprofile.timer=1 -serial stdio'
          ]


class TestGeniviQemu(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.kvm = Popen(kvmCmd)
        self.arch=arch
        self.port = port
        # pid = kvm.pid
        #print kvm.returncode
        if (self.kvm.returncode != None):
            assert False, "Could not start image"
        time.sleep(sleepBeforeTime) # semi random number! need to sleep so that kvm has started and port 5555 is open
                      # if it is too short then ssh waits for a retry which may result in the test taking longer!
    @classmethod
    def tearDownClass(self):
        # should this be tearDown? maybe want to test the system is down afterwards?
        # see test_restart for a poweroff test
        if (self.kvm != None):
            call(baseSsh + ["poweroff"])

    # Two helper functions        
    def makeTest(self, cmd, expected):
        """Call this function with the shell command you want running  on the image (cmd)
        and the expected result (expected) """
        cmdValues = cmd.split(' ')
        result = self.sendCommand(cmdValues)
        return (result == expected)
    
    def sendCommand(self,cmd):
        """ Expects a list parameter containing the arguments of the command to be executed on the
        target. Returns the output.
        e.g. self.sendCommand(['df', '/tmp'])
        """
        op = check_output(baseSsh +cmd)
        return op


    

if __name__ == '__main__':
    # start the image

    gensuite = unittest.TestLoader().loadTestsFromTestCase(TestGeniviQemu)
    unittest.TextTestRunner(verbosity=2).run(gensuite)


    
