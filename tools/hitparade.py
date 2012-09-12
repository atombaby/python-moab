#!/usr/bin/env python
# Show current cluster utilization grouped by user
# User, Cores
# pbradley 954
# rfu 150
# ylin2 110
# sjiao 101
# cqu 100
# ckang2 16
# syin2 2
# krcurtis 1
# Free 62
# Total 1496


from scheduler import Scheduler
from mtypes import Job
import xml.etree.ElementTree as et
import operator

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
        summary[ job.User ] = summary[ job.User ] + job.ReqProcs
    except KeyError:
        summary[ job.User ] = job.ReqProcs


ofmt="{:>15} {}"
print ofmt.format( 'user', 'cores' )
for k,v in sorted( summary.iteritems(),
        key=operator.itemgetter(1),
        reverse=True):
    print ofmt.format( k, v )

ofmt="{:>15} {} of {}"
print ofmt.format( 'free nodes', free_nodes, up_nodes )
print ofmt.format( 'free cores', free_cores, up_cores )
