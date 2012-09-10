#!/usr/bin/env python
# Show current cluster utilization grouped by account and user
# account user cores
#         user cores
# oacct   user cores
#         user cores


from scheduler import Scheduler
from mtypes import Job
import xml.etree.ElementTree as et

s = Scheduler()
summary = {}

r = et.fromstring(
    s.doCommand( [ "showq", "--xml", '-r', ] )
)

# Used/free stats are in the "cluster" branch

free_nodes = r.find( 'cluster' ).attrib[ 'LocalIdleNodes' ]
up_nodes = r.find( 'cluster' ).attrib[ 'LocalUpNodes' ]
free_cores = r.find( 'cluster' ).attrib[ 'LocalIdleProcs' ]
up_cores = r.find( 'cluster' ).attrib[ 'LocalUpProcs' ]

for j in r.findall( 'queue/job' ):
    job = Job( j.attrib )
    try:
        if summary[ job.Account ]:
            pass
    except KeyError:
        summary[ job.Account ] = {}

    try:
        summary[ job.Account ][ job.User ] = ( 
            summary[ job.Account ][ job.User ] + job.ReqProcs )
    except KeyError:
        summary[ job.Account ][ job.User ] = job.ReqProcs


ofmt="{:>20} {:.>15} {}"
print ofmt.format( 'account', 'user', 'cores' )
for acct in summary.keys():
    a_tmp = acct
    for k,v in summary[ acct ].items():
        print ofmt.format( a_tmp, k, v )
        a_tmp = ''

ofmt="{:>15} {} of {}"
print ofmt.format( 'free nodes', free_nodes, up_nodes )
print ofmt.format( 'free cores', free_cores, up_cores )


print summary
