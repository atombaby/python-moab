#!/usr/bin/env python

from scheduler import Scheduler
from mtypes import Reservation, Job
import xml.etree.ElementTree as et

s = Scheduler()
summary = {}

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

for q in r.findall( 'job' ):
    job_details= q.attrib
    job_details.update( q.find( 'req' ).attrib )
    j = Job( job_details )
    if j.State == 'Running':
        print '-' * 80
        prv_core_count = 0
        oth_core_count = 0
        prv_nodes = set(j.AllocNodeList.keys()).intersection( set(reserved_nodes.keys()) )
        other_nodes = set(j.AllocNodeList.keys()).difference( set(reserved_nodes.keys()) )

        print "JobID: {}".format( j.JobID, )
        print "Account: {}".format( j.Account, )
        print "User: {}".format( j.User, )
        for m in prv_nodes:
            if reserved_nodes[ m ] == 0 :
                prv_core_count = prv_core_count + 12
            else:
                prv_core_count = prv_core_count + reserved_nodes[ m ]
        print "Private Cores/Nodes: {}/{}".format( prv_core_count, prv_nodes )
        for m in other_nodes:
            if j.AllocNodeList[ m ] == 0 :
                oth_core_count = oth_core_count + 12
            else:
                oth_core_count = oth_core_count + j.AllocNodeList[ m ]
        print "Other Cores/Nodes: {}/{}".format( oth_core_count, other_nodes )

