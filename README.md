# genivi-testing
Test scripts

Scripts to enable the automatic testing of QEMU genivi images.
They will eventually need integrating within the yocto/GENIVI system

There are 2 user invocable files runOneTest.py and runAllTests.py

runOneTest.py expects a test name to be supplied, currently only a python
file (without the .py suffix), see the example files in unitTests as an indication
of how to derive new ones. The class in each test file should inherit from geniviTest.TestGeniviQemu
The test method must have a name with a test_ prefix. More than one test file can
be supplied on the comment line

runAllTests.py runs all the tests it finds in unitTests as well as a set of tests in coreTests.py

The infrastructure handles booting the QEMU image. It is assumed that
the tests are run from the gdp-src-build directory though if you set
the QEMU_IMAGE_DIR environment variable you can test on images
elsewhere - or ones you have downloaded from the GENIVI download area.
The test infrastructure looks for a bzImage file in the appropriate locations and a file
system in genivi-dev-platform-qemux86-64.ext4
The image shuts down automatically after all tests have been run.

It is also assumed that the QEMU image is built without a password for
logging in as root - build with EXTRA_USERS_PARAMS = "", if you
install sshpass you can test against images with passwords - set the
environment variable QEMU_USER_SSHPASS to signal this - the password
'root' is assumed.

If you with to boot the virtual machine with other options - it
redirects the ssh port to 5555 - examine the preface to geniviTest.py