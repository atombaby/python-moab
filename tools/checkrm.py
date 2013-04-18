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
#sys.path.insert( 0, '/opt/moab/lib/python2.7/site-packages' )
sys.path.insert( 0, '/home/mrg/build/python-moab' )
import os
os.environ['PATH']= '/opt/moab/bin/:' + os.environ['PATH']

from mwm.scheduler import Scheduler
from mwm.queue import getIdleJobSummary

CRITICAL = 2
WARNING = 1
OK = 0
pmsg = [ 'OK', 'WARNING', 'CRITICAL' ]


def update( cval, nval ):
    if nval > cval:
        return nval
    else:
        return cval

try:
    s = Scheduler()
except:
    print "UNABLE TO CONNECT TO SCHEDULER"
    sys.exit( CRITICAL )

message = []
xtv = OK

state = s.getRMData()['STATE']

if state == 'Active' and s.state == 'RUNNING':
    message.append( "RM and Scheduler running" )
    xtv = update( xtv, OK )

elif state == 'Active' and s.state != 'RUNNING':
    message.append( "SCHEDULER NOT RUNNING" )
    xtv = update( xtv, OK )

elif state != 'Active' and s.state == 'RUNNING':
    message.append( "RESOURCE MANAGER NOT ACTIVE".format( state, s.state ) )
    xtv = update( xtv, CRITICAL )

elif state != 'Active' and s.state != 'RUNNING':
    message.append(
        "UNKNOWN CONDITION... RM is {}. Scheduler is {}".format(
            state, s.state )
    )
    xtv = update( xtv, CRITICAL )

if xtv != OK:
    # Critical and/or warnings at this point preclude
    # successful execution of following checks, so bail
    # out now
    print ": ".join( [ pmsg[ xtv ] ] + message )
    sys.exit( xtv )

idlejob = getIdleJobSummary( s )
if len( idlejob ) > 0:
    message.append( "{} IDLE JOBS FOUND".format( len(idlejob) ) )
    xtv = update( xtv, WARNING )


print ": ".join( [ pmsg[ xtv ] ] + message )
sys.exit( xtv )
