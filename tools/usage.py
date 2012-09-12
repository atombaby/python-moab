#!/usr/bin/env python

from scheduler import Scheduler
from mtypes import Reservation, Job, Node
import xml.etree.ElementTree as et

s = Scheduler()
summary = {}

# Joe User using 12 cores on one private node, 24 on 4 public nodes
# Account for Joe User (user_j) with Bob Barker using 24 cores on 4 public nodes and Alice Alignment using 12 cores on one private node
# 
# each account has records like:
# AS {
# 'name': 'user_j'
# {
#   'aa': { 'private':[ 1, 12 ], 'public':[ 0, 0 ] },
#   'bb': { 'private':[ 0, 0 ], 'public':[ 4, 24 ] }
# }
#}

# account_summary.getNodeTotal() = [ n, m ] where
# n is the sum of private nodes in use for all users and m
# the sum of all public nodes

class AS():
    def __init__(self, name):
        self.name = name
        self.users = {}
        pass
    
    def _create_user( self, user ):
        if user not in self.users:
            self.users[ user ] = {'private':[0,0], 'public':[0,0] }
        else:
            pass

    def addJob(self, user, pvnodes=0, pvcores=0, pbnodes=0, pbcores=0 ):
        self._create_user( user )
        self.users[ user ][ 'private' ][0] += pvnodes
        self.users[ user ][ 'private' ][1] += pvcores
        self.users[ user ][ 'public' ][0] += pbnodes
        self.users[ user ][ 'public' ][1] += pbcores

    def summary( self ):
        pvn = 0
        pvc = 0
        pbn = 0
        pbc = 0
        for user in self.users:
            pvn = pvn + self.users[ user ]['private'][0]
            pvc = pvc + self.users[ user ]['private'][1]
            pbn = pbn + self.users[ user ]['public'][0]
            pbc = pbc + self.users[ user ]['public'][1]
        return [ pvn, pvc, pbn, pbc ]

    def userSummary( self, user ):
        return[
            self.users[ user ]['private'][0],
            self.users[ user ]['private'][1],
            self.users[ user ]['public'][0],
            self.users[ user ]['public'][1],
        ]


r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-r', ] )
)

reserved_nodes = {}

for q in r.findall( 'rsv' ):
    rsv = Reservation( q.attrib )
    if 'STANDINGRSV' in rsv.flags:
        reserved_nodes.update( rsv.AllocNodeList )

r = et.fromstring(
    s.doCommand( [ "mdiag", "--xml", '-j', ] )
)

# total = {'acctname':AS()}}
total = {}

for q in r.findall( 'job' ):
    job_details= q.attrib
    job_details.update( q.find( 'req' ).attrib )
    j = Job( job_details )
    if j.State == 'Running':
        prv_core_count = 0
        oth_core_count = 0

        prv_nodes = set(j.AllocNodeList.keys()).intersection(
            set(reserved_nodes.keys()) )
        other_nodes = set(j.AllocNodeList.keys()).difference(
            set(reserved_nodes.keys()) )


        if j.Account not in total:
            total[ j.Account ] = AS( j.Account )

        for m in prv_nodes:
            if reserved_nodes[ m ] == 0 :
                prv_core_count = prv_core_count + 12
            else:
                prv_core_count = prv_core_count + reserved_nodes[ m ]
        for m in other_nodes:
            if j.AllocNodeList[ m ] == 0 :
                oth_core_count = oth_core_count + 12
            else:
                oth_core_count = oth_core_count + j.AllocNodeList[ m ]

        total[ j.Account ].addJob(
            j.User,
            len( prv_nodes ),
            prv_core_count,
            len( other_nodes ),
            oth_core_count,
        )

ofmt = "{:>25}{:^15}{:^15}"
print ofmt.format( "user", "private", "public" )
ofmt = "{:>25}{:>6} / {:<4}{:>6} / {:<4}"
print ofmt.format( "account total","nodes", "cores","nodes", "cores" )
print "-" * 53

pvn_total = 0
pvc_total = 0
pbn_total = 0
pbc_total = 0
for acct, smry in total.items():
    ofmt = "{:>25}{:>6} / {:<5}{:>6} / {:<5}"
    for u in smry.users:
        t = smry.userSummary(u)
        print ofmt.format(
            u, *(smry.userSummary(u)) )

    ofmt = "{:>25}{:>6} / {:<5}{:>6} / {:<5}"
    print ofmt.format( acct + " total", *(smry.summary()) )
    print "-" * 53

    pvn_total = pvn_total + smry.summary()[0]
    pvc_total = pvc_total + smry.summary()[1]
    pbn_total = pbn_total + smry.summary()[2]
    pbc_total = pbc_total + smry.summary()[3]

print ofmt.format( "total used", pvn_total, pvc_total, pbn_total, pbc_total )

r = et.fromstring( s.doCommand( [ "mdiag", "--xml", "-n" ] ) )

pvn_total = 0
pvc_total = 0
pbn_total = 0
pbc_total = 0
for node_entry in r.findall( 'node' ):
        n = Node( node_entry.attrib )
        if n.NODEID not in reserved_nodes and n.RAPROC > 0:
            pbc_total += n.RAPROC
            pbn_total += 1
        elif n.NODEID in reserved_nodes and n.RAPROC > 0:
            pvc_total += n.RAPROC
            pvn_total += 1

ofmt = "{:>25}{:>6} / {:<5}{:>6} / {:<5}"
print ofmt.format( "total available", pvn_total, pvc_total, pbn_total, pbc_total )

