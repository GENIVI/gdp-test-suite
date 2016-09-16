#!/usr/bin/python
import unittest
from subprocess import call, Popen, check_output
import time
import os


# variables which might need changing
Arch='qemux86-64'
fs='genivi-dev-platform-'+Arch+'.ext4'
image='bzImage'
Port = '5555'
sleepBeforeTime = 6 # time to sleep to allow vm to start, too short and it may fail, make it long enough
                    # to try to align the vm and the tests, also if short the ssh may wait to retry making
                    # the test time longer!
# end of configurable area

# the user can set the environment varible QEMU_IMAGE_DIR to determine
# the directory containing the kernel/disk image
if  (os.environ.has_key('QEMU_IMAGE_DIR')):
    dir = os.environ['QEMU_IMAGE_DIR'] + '/'
else:
    # this is probably no longer right if the script is being run from their directory?
    dir='tmp/deploy/images/'+Arch+'/'

if not os.path.isfile(dir+image) :
    print fs
    raise Exception("Image file not found - do you need to set QEMU_IMAGE_DIR?")

def finalizer_function():
    print 'run once'
    
# @unittest.fixture(scope="session", autouse=True)
# def do_something(request):
#     # prepare something ahead of all tests
#     request.addfinalizer(finalizer_function)
    
# Assumes that the image has been built with EXTRA_USERS_PARAMS = ""
# If it hasn't you may need to install sshpass and edit the parameters!
baseSsh = ['ssh', '-o', 'StrictHostKeyChecking=no', 'root@127.0.0.1', '-p', Port, '-o', 'ConnectTimeout=7',
           '-o', 'BatchMode=yes']

kvmCmd = [
          'kvm', '-kernel', dir+image, '-net', 'nic',
          '-net', 'user,hostfwd=tcp::'+Port+'-:22', # open port 5555 for ssh access
          '-cpu', 'core2duo',
          '-hda', dir+fs, 
          '-vga', 'std',  '-no-reboot', '-m', '512',
          '--append', 'vga=0 uvesafb.mode_option=640x480-32 root=/dev/hda rw mem=512M  oprofile.timer=1 -serial stdio'
          ]
# def setUpModule():
#     print 'running'
#     TestGeniviQemu.setUpKvm()
# def tearDownModule():
#     TestGeniviQemu.tearDownKvm()

class TestGeniviQemu(unittest.TestCase):
    kvm = 0
    arch = ''
    port = 0
    @staticmethod
    def poweron():
        TestGeniviQemu.kvm = Popen(kvmCmd)
        TestGeniviQemu.arch=Arch
        TestGeniviQemu.port = Port
        # pid = kvm.pid
        #print kvm.returncode
        if (TestGeniviQemu.kvm.returncode != None):
            assert False, "Could not start image"
        time.sleep(sleepBeforeTime) # semi random number! need to sleep so that kvm has started and port 5555 is open
                      # if it is too short then ssh waits for a retry which may result in the test taking longer!
    @staticmethod
    def poweroff():
        # should this be tearDown? maybe want to test the system is down afterwards?
        # see test_restart for a poweroff test
        if (TestGeniviQemu.kvm != None):
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
    print 'This is no longer the testing top level'
    print '    use runAllTests.py or runOneTest.py instead!'


    
