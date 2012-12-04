#!/usr/bin/env python
"""
Show used and available public cores. Break down used
cores by user and account
"""
import sys
import logging
import argparse
import xml.etree.cElementTree as et


parser = argparse.ArgumentParser( description = 'show cluster users' )
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


node_reservations = {}
r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-r', ] )
)
for q in r.findall( 'rsv' ):
    rsv = Reservation( q.attrib )
    if rsv.Type == "User" and rsv.SubType == "StandingReservation":
        logging.debug( "Found standing reservation: %s", rsv.Name )
        for n in rsv.AllocNodeList:
            node_reservations[ n ] = rsv.RsvParent
            logging.debug( "Added node %s to reserved node list", n )

r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-j', ] )
)

jobs = {}
for j in r.findall( 'job' ):
    job = Job( dict( j.attrib.items() + j.find('req').items() ))
    if job.State == 'Running' and "PREEMPTEE" not in job.Flags:
        jobs[ job.JobID ] = [
            job.AllocNodeList,
            job.User,
            job.Account,
        ]

# create count of public nodes in campus class
r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-n', ] )
)

public_nodes = []
public_cores = 0
logging.debug( "Looking for public nodes" )
for n in r.findall( 'node' ):
    node = Node( n.attrib )
    if 'campus' not in node.CFGCLASS:
        logging.debug( "node %s not in campus class", node.NODEID )
        continue
    if node.NODEID in node_reservations:
        logging.debug( "node %s in private reservation %s", node.NODEID, node_reservations[ node.NODEID ] )
        continue

    logging.debug( "node %s added to public list",  node.NODEID )
    public_nodes.append( node.NODEID )
    public_cores += node.RCPROC

cred_totals = {}
# { 'cred':cores }
for job in jobs.values():
    logging.debug( "Counting job with creds %s", job )
    for node in job[0]:
        job_cred = job[1] + " (" + job[2] + ")"
        if node in public_nodes:
            o = [
                job[0][node],
                node,
                'public',
                job_cred,
            ]
            try:
                cred_totals[ job_cred ] = (
                    cred_totals[ job_cred ] + job[0][node]
                )
            except KeyError:
                cred_totals[ job_cred ] = job[0][node]

print "{:>25} {:<5}".format( 'user (account)', 'cores' )
print "{:->25} {:-<5}".format( '', '' )

sum = 0
for k,v in sorted( cred_totals.items(), key=lambda x: x[1], reverse=True):
    print "{:>25} {:<5}".format( k,v )
    sum += v

print "{:->25} {:-<5}".format( '', '' )
print "{:>25} {:<5}".format( 'total cores configured', public_cores )
print "{:>25} {:<5}".format( 'total cores in use', sum )
print "{:>25} {:<5}".format( 'total cores available', public_cores - sum )

