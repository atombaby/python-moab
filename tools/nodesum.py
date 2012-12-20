#!/usr/bin/env python
"""
Show breakdown of nodes in use

name         reserved  in use      preemptable  idle
------------ --------- ----------  -----------  ----------
gizmod1234   resv_name 3           9            0
gizmoc1235   -         0           0            12
gizmoc1236   -         2           0            10*

* indicates naccesspolicy != shared
"""
import sys
import logging
import argparse
import xml.etree.cElementTree as et


def gx( hname ):
    # split a cluster hostname in to the
    # base and index (gizmo123 -> [ 'gizmo', 123 ])
    x = ""
    for n in range(len(hname)-1, 0, -1):
        if hname[n].isdigit():
            x = hname[n] + x 
        else:
            return [ hname[:n+1], int(x) ]

parser = argparse.ArgumentParser( description = 'Show cluster node utilization' )
parser.add_argument( '--debug', action='store_true', default=False )
argv = parser.parse_args()

if argv.debug:
    logging.basicConfig( level=logging.DEBUG )
    print argv.debug
else:
    logging.basicConfig( level=logging.WARNING )

try:
    from mwm.scheduler import Scheduler
    from mwm.mtypes import Reservation, Job, Node
except ImportError:
    logging.exception( "Moab client libraries not found" )
    sys.exit(1)

s = Scheduler()

# Collect reservations
# { reservation name:mwm.Reservation.Name }
reservations = {}
r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-r', ] )
)

for q in r.findall( 'rsv' ):
    rsv = Reservation( q.attrib )
    reservations[ rsv.Name ] = rsv
    logging.debug( "Added reservation: %s", rsv.Name )

# Collect jobs
# { jobid:mwm.Job.JobID }
jobs = {}
r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-j', ] )
)

for q in r.findall( 'job' ):
    job = Job( dict( q.attrib.items() + q.find('req').items() ))
    if job.State == 'Running':
        jobs[ job.JobID ] = job

# Collect Nodes
# { node name: mwm.Node.NODEID }
nodes = {}
r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-n', ] )
)

logging.debug( "Looking for public nodes" )
for q in r.findall( 'node' ):
    node = Node( q.attrib )
    if 'campus' not in node.CFGCLASS:
        logging.debug( "node %s not in campus class", node.NODEID )
        continue
    logging.debug( "node %s added to list",  node.NODEID )
    nodes[ node.NODEID ] = node

# result[name] = [ alloc, preempt, available, special, reserved ]
# alloc : integer indicating allocated  processors
# preemptable: integer indicating allocated preemptable processors
# available : integer indicating processors available on node
# special: boolean indicating special restriction such as
#          accesspolicy)
# reserved: parent-group of standing reservation
result = {}
for node in nodes.values():
    # find reservations on node
    # intialize result
    logging.debug( "initialized result for %s", node.NODEID )
    result[ node.NODEID ] = [ 0, 0, node.RCPROC, '', '' ]

    for reservation in reservations.values():
        if (
            reservation.SubType == 'StandingReservation' and
            'ISACTIVE' in reservation.flags and
            reservation.AllocNodeList.has_key( node.NODEID )
        ):
            logging.debug( "%s part of standing reservation %s",
                          node.NODEID, reservation.RsvParent )
            result[ node.NODEID ][4] = reservation.RsvParent

    for job in jobs.values():
        if job.AllocNodeList.has_key( node.NODEID ):
            logging.debug( "%s in job %s", node.NODEID, job.JobID )
            result[ node.NODEID ][0] = (
                result[ node.NODEID ][0] +
                job.AllocNodeList[ node.NODEID ] )
            logging.debug( "set procs in use to %s",
                          result[ node.NODEID ][0])

            logging.debug( "Job flags are %s", job.Flags )
            if 'PREEMPTEE' in job.Flags:
                result[ node.NODEID ][1] = (
                    result[ node.NODEID ][1] +
                    job.AllocNodeList[ node.NODEID ] )
            logging.debug( "Job node access policy is %s", job.NodeAccess )

            if job.NodeAccess != "SHARED":
                result[ node.NODEID ][3] = job.NodeAccess

fmt2 = '{:-<12}{:-<5}{:-<5}{:-<5} {:-<5}'
fmt = '{:<12}{:>5}{:>5}{:>5} {:>5}'
print fmt.format('name', 'used', 'prmt', 'idle', 'resv')
print fmt2.format( '', '', '', '', '' )
for k in sorted( result.iterkeys(), key=lambda f: gx(f) ):
    v = result[k]
    if v[3] != "":
        restriction = v[3]
    elif v[4] != "":
        restriction = v[4]
    else:
        restriction = ""

    print fmt.format( k, v[0], v[1], v[2] - v[0], restriction )

