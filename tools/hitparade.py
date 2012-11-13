#!/usr/bin/env python
"""
Show used and available public cores. Break down used
cores by user and account
"""
import sys
sys.path.append('/opt/moab/lib/python2.7/site-packages')
from mwm.scheduler import Scheduler
from mwm.mtypes import Reservation, Job, Node
import xml.etree.cElementTree as et

bold='\033[1;47m'
normal='\033[1;m'

s = Scheduler()


node_reservations = {}
r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-r', ] )
)
for q in r.findall( 'rsv' ):
    rsv = Reservation( q.attrib )
    if rsv.Type == "User" and rsv.SubType == "StandingReservation":
        for n in rsv.AllocNodeList:
            node_reservations[ n ] = rsv.RsvParent

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
for n in r.findall( 'node' ):
    node = Node( n.attrib )
    if 'campus' in node.CFGCLASS and node.NODEID not in node_reservations:
        public_nodes.append( node.NODEID )
        public_cores += node.RCPROC

cred_totals = {}
# { 'cred':cores }
for job in jobs.values():
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

