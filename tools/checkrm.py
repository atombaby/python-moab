#!/usr/bin/env python

#
# Nagios Plugin for MWM

# Checks the scheduler and resource manager on the local
# system.  Both must be running else the plugin notes a
# critical error.
#
# Requires the python-moab plugin:
#   https://github.com/atombaby/python-moab
#

import sys
sys.path.insert( 0, '/opt/moab/lib/python2.7/site-packages' )
import os
os.environ['PATH']= '/opt/moab/bin/:' + os.environ['PATH']

from mwm.scheduler import Scheduler

CRITICAL = 2
WARNING = 1
OK = 0

try:
	s = Scheduler()
except:
	print "UNABLE TO CONNECT TO SCHEDULER"
	sys.exit( CRITICAL )

state = s.getRMData()['STATE']
if state == 'Active' and s.state == 'RUNNING':
	print "OK: RM is {}. Scheduler is {}".format( state, s.state )
	sys.exit( OK )
elif state == 'Active' and s.state != 'RUNNING':
	print ( "SCHEDULER NOT RUNNING: "
        "RM is {}. Scheduler is {}".format( state, s.state ) )
	sys.exit( CRITICAL )
elif state != 'Active' and s.state == 'RUNNING':
	print ( "RESOURCE MANAGER NOT ACTIVE: "
        "RM is {}. Scheduler is {}".format( state, s.state ) )
	sys.exit( CRITICAL )
else:
	print ( "UNKNOWN CONDITION: "
        "RM is {}. Scheduler is {}".format( state, s.state ) )
	sys.exit( CRITICAL )



