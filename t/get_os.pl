#!/usr/bin/perl -w

# Name:             get_os.pl
# Purpose:          Demonstrate TAP

use strict;
use Test::More tests => 3;

diag("$0");
require_ok( 'Test::Harness' );
is("$]", "5.020002", 'Perl version 5.20.0');
ok($^O eq 'linux', 'Operating system is correct');
