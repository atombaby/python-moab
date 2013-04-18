#!/usr/bin/env python

# show interesting things about a queue

import scheduler
import sys
import xml.etree.ElementTree as et

def getRunningJobs( s ):
    # return running jobs as array of hashes
    pass

def getRunningSummary( s ):
    # return summary statistics on running jobs
    summary = {}
    command = [ "showq", "--xml", '-r' ]
    
    queue = et.fromstring( s.doCommand( command ) )

    job_total = queue.find( 'queue' ).attrib[ 'count' ]
    processors = queue.find( "cluster" ).attrib[ 'LocalAllocProcs' ]
    nodes = queue.find( "cluster" ).attrib[ 'LocalActiveNodes' ]

    for j in queue.findall( 'queue/job' ):
        a = j.attrib[ 'Account' ]
        p = int( j.attrib[ 'ReqProcs' ] )
        wc = (
            float( j.attrib[ 'ReqAWDuration' ] ) -
            float( j.attrib[ 'StatPSDed' ] ) )
        if wc < 0:
            wc = -wc
        ps = p * wc
        print "account {}, procs {}, time {}, ps {}".format( a, p, wc, ps )

        try:
            summary[ a ][ 'procs' ] = summary[ a ][ 'procs' ]  + p
            summary[ a ][ 'wc' ] = summary[ a ][ 'wc' ]  + wc
            summary[ a ][ 'ps' ] = summary[ a ][ 'ps' ]  + ps
        except KeyError:
            summary[ a ] = {}
            summary[ a ][ 'procs' ] = p
            summary[ a ][ 'wc' ] = wc
            summary[ a ][ 'ps' ] = ps

    return summary

def getIdleJobSummary( s ):
    command = [ "showq", "--xml", '-i' ]
    queue = et.fromstring( s.doCommand( command ) )
    retval = []
    for j in queue.findall( 'queue/job' ):
        retval.append( j.attrib[ 'JobID' ] )
    return retval

def main():
    s = scheduler.Scheduler()
    print s.state
    summary = getRunningSummary( s )
    for acct in summary.keys():
        print acct, summary[ acct ][ 'procs' ]

    getIdleJobSummary( s )
        

if __name__ == '__main__':
    status = main()
    sys.exit(status)
