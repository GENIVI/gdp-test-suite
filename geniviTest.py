#!/usr/bin/python
import unittest
from subprocess import call, Popen, check_output
import time

# variables which might need changing
dir='tmp/deploy/images/qemux86-64/'
fs='genivi-dev-platform-qemux86-64.ext4'
image='bzImage'
port = '5555'

# Assumes that the image has been built with EXTRA_USERS_PARAMS = ""
# If it hasn't you may need to install sshpass and edit the parameters!
baseSsh = ['ssh', '-o', 'StrictHostKeyChecking=no', 'root@127.0.0.1', '-p', port]

kvmCmd = [
          'kvm', '-kernel', dir+image, '-net', 'nic',
          '-net', 'user,hostfwd=tcp::'+port+'-:22', # open port 5555 for ssh access
          '-cpu', 'core2duo',
          '-hda', dir+fs, 
          '-vga', 'vmware',  '-no-reboot', '-m', '512',
          '--append', 'vga=0 uvesafb.mode_option=640x480-32 root=/dev/hda rw mem=512M  oprofile.timer=1 -serial stdio'
          ]

# def setUpModule():
#     pid = Popen(kvmCmd).pid
#     time.sleep(4) # semi random number! need to sleep so that kvm has started and port 5555 is open
#                   # if it is too short then ssh waits for a retry which may result in the test taking longer! 

# def tearDownModule():
#     # should this be tearDown? maybe want to test the system is down afterwards?
#     call(baseSsh + ["poweroff"])


class TestGeniviQemu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pid = Popen(kvmCmd).pid
        time.sleep(4) # semi random number! need to sleep so that kvm has started and port 5555 is open
                  # if it is too short then ssh waits for a retry which may result in the test taking longer! 
    @classmethod
    def tearDownClass(cls):
        # should this be tearDown? maybe want to test the system is down afterwards?
        call(baseSsh + ["poweroff"])
    def test_checkErrors(self):
        # tests for errors on startup, searching the output of dmesg for occurrences of the word error
        op = check_output(baseSsh + ['dmesg',' |', 'grep', 'error', '|', 'wc', '-l'] )
        self.assertEqual(int(op),0)

    def test_checkQemu(self):
        # looks for a qemux architecture in the dmesg output
        op = check_output(baseSsh + ['dmesg', '-t', '|', 'grep', 'qemux'])
        self.assertEqual(op[0:-1],'systemd[1]: Set hostname to <qemux86-64>.') # trim EOL
        #op = check_output(baseSsh + ['dmesg',' |', 'grep', 'qemux' , ' |',  'awk {print $NF}' ], shell=True)
        #self.assertEqual(op,'<qemux86-64>.') #'Set hostname to <qemux86>.') # trim prefix

    def test_checkSystemCtl(self):
        # check weston is running
        op = check_output(baseSsh + ['systemctl', 'is-active', 'weston'])
        self.assertEqual(op, 'active\n')

    # this test seems to run last so no need for a restart??
    # and a test to timeout because it is shutdown?
    @unittest.expectedFailure
    def test_restart(self):
        call(baseSsh + ["poweroff"])
        time.sleep(4)
        op = check_output(baseSsh, "uptime")
        pid = Popen(kvmCmd).pid
        time.sleep(4) # just in case something else happens?
        
    def untest_checkSystemCtlActive(self):
        # checks the number of active system services (is this too prescriptive?
        op = check_output(baseSsh + ['systemctl', '|', 'grep', 'active', '|', 'grep', 'inactive']) #, '|', 'grep', '362'])
        #print "<", op, ">" hmm is it really const?
        self.assertEqual(int(op.split(None, 1)[0]), 362)
        # '362 loaded units listed. Pass --all to see loaded but inactive units, too.')

    

if __name__ == '__main__':
    # start the image

    gensuite = unittest.TestLoader().loadTestsFromTestCase(TestGeniviQemu)
    unittest.TextTestRunner(verbosity=2).run(gensuite)

#    call(baseSsh + ["poweroff"])

    
