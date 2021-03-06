#!/usr/bin/env python
"""
Show used and available public cores. Break down used
cores by user and account
"""
import sys
import logging
import argparse
import xml.etree.cElementTree as et
import csv
from mwm.scheduler import Scheduler
from mwm.mtypes import Reservation, Job, Node


def main():
    """
    Do some stuff, eventually printing output to stdout...
    """
    # Parse command-line arguments
    arguments = parse_arguments()

    # Logging setup
    if arguments.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    node_reservations = get_node_reservations()
    jobs = get_jobs(all_jobs=arguments.all_jobs)
    cred_totals, public_cores, public_nodes, public_nodes_free = get_counts(node_reservations, jobs)
    if arguments.free_cores:
        print_free_cores(cred_totals, public_cores)
    elif arguments.csv:
        print_csv(arguments.csv_header_suppress, cred_totals, public_cores, public_nodes, public_nodes_free)
    else:
        print_output(cred_totals, public_cores, public_nodes, public_nodes_free) 

def is_private( rsv ):
    """
    A private reservation is
    a) not of type "User" or "Job"
    b) subtype of StandingReservation
    c) not in the reservation group "iactive" or largenode
    """
    if rsv.Type == "Job":
        logging.debug( "reservation: %s is job reservation", rsv.Name )
        return False
    if rsv.RsvGroup == "iactive" or rsv.RsvGroup == "largenode":
        logging.debug( "reservation: %s is public reservation", rsv.Name )
        return False
    if rsv.SubType == "Other" and rsv.Type == "User":
        logging.debug( "%s is non-private reservation", rsv.Name )
        return False
    if rsv.SubType == "StandingReservation" and rsv.Type == "User":
        logging.debug( "%s is private reservation", rsv.Name )
        return True

    logging.debug( "reservation %s assumed private", rsv.Name )
    return True

def get_node_reservations():
    """
    Return a dictionary where node is the key and RsvParent 
    is the value.  Reservation must be Type == User and 
    have a SubType of StandingReservation.
    """
    s = Scheduler()
    # Dictionary where 
    node_reservations = {}

    # Command to execute that returns some xml, initializes element tree.
    r = et.fromstring(
        s.doCommand( [ "mdiag", "--xml", '-r', ] )
    )

    # Element tree has data at the root, and likely 1 or more rsv children.
    for q in r.findall( 'rsv' ):
        # Instantiate a Reservation, where xml attributes map to object properties.
        # q.attrib is a dictionary of attributes and their values.
        rsv = Reservation( q.attrib )
        #if rsv.Type == "User" and rsv.SubType == "StandingReservation" and rsv.RsvGroup != "iactive":
        #if not is_private( rsv ):
        if is_private( rsv ):
            logging.debug( "Found reservation: %s", rsv.Name )
            for n in rsv.AllocNodeList:
                # Question here, any chance more than one reservation
                # could include the same node, but with different 
                # RsvParents?  Last in wins?
                node_reservations[ n ] = rsv.RsvParent
                logging.debug( "Added node %s to reserved node list", n )

    return node_reservations


def get_jobs(all_jobs=False):
    """
    Build up a dictionary of jobs.  Key is job_id, value is
    a list containing AllocNodeList, User and Account.
    """
    s = Scheduler()
    r = et.fromstring(
        s.doCommand( [ "mdiag", "--xml", '-j', ] )
    )

    jobs = {}
    for j in r.findall( 'job' ):
        job = Job( dict( j.attrib.items() + j.find('req').items() ))
        # Add all running jobs if --all, otherwise filter out preemptees.
        if (job.State == 'Running' and all_jobs) or \
           (job.State == 'Running' and "PREEMPTEE" not in job.Flags and not
           all_jobs): 
            jobs[ job.JobID ] = [
                job.AllocNodeList,
                job.User,
                job.Account,
            ]
    return jobs


def get_counts(node_reservations, jobs):
    """
    Provide counts for total public core usage and 
    broken down by user and account.
    """
    s = Scheduler()

    # create count of public nodes in campus class
    r = et.fromstring(
        s.doCommand( [ "mdiag", "--xml", '-n', ] )
    )

    public_nodes = []
    public_cores = 0
    logging.debug( "Looking for public nodes" )
    for n in r.findall( 'node' ):
        node = Node( n.attrib )
        # When node.CFGCLASS does not contain 'campus', this is not a public
        # node. Also skip if node has an associated reservation. Node 
        # is added to public_nodes list in all other cases.
        if node.NODESTATE == 'Drained' or node.NODESTATE == 'Down':
            logging.debug( "node %s is %s", node.NODEID, node.NODESTATE )
            continue
        if 'campus' not in node.CFGCLASS:
            logging.debug( "node %s not in campus class", node.NODEID )
            continue
        if node.NODEID in node_reservations:
            logging.debug( "node %s in private reservation %s", node.NODEID, node_reservations[ node.NODEID ] )
            continue

        public_nodes.append( node.NODEID )
        logging.debug( "node %s added to public list",  node.NODEID )
        public_cores += node.RCPROC
        logging.debug( "added %s cores from node %s added to public core total", node.RCPROC, node.NODEID )

    cred_totals = {}
    # { 'cred':cores }
    # Copy the list to later subtract in-use nodes.
    public_nodes_free = public_nodes[:]
    for job in jobs.values():
        logging.debug( "Counting job with creds %s", job )
        for node in job[0]:
            job_cred = job[1] + " (" + job[2] + ")"
            if node in public_nodes:
                logging.debug( "node %s is public", node )
                o = [
                    job[0][node],
                    node,
                    'public',
                    job_cred,
                ]
                # Remove public nodes that have at least one 
                # core in use from public_nodes_free
                if node in public_nodes_free: 
                    del public_nodes_free[public_nodes_free.index(node)]
                try:
                    cred_totals[ job_cred ] = (
                        cred_totals[ job_cred ] + job[0][node]
                    )
                except KeyError:
                    cred_totals[ job_cred ] = job[0][node]

    logging.debug( "Nodes Free: %s", public_nodes_free )
    logging.debug( "Cred totals: %s", cred_totals )
    return cred_totals, public_cores, len(public_nodes), len(public_nodes_free)


def print_free_cores(cred_totals, public_cores):
    """
    """
    total = 0
    for k,v in sorted( cred_totals.items(), key=lambda x: x[1], reverse=True):
        total += v
    sys.stdout.write(str(public_cores - total))


def print_output(cred_totals, public_cores, public_nodes, public_nodes_free):
    """
    Display totals to stdout, sorted descending by core count.
    """
    print "{:>25} {:<5}".format( 'user (account)', 'cores' )
    print "{:->25} {:-<5}".format( '', '' )

    for k,v in sorted( cred_totals.items(), key=lambda x: x[1], reverse=True):
        print "{:>25} {:<5}".format( k,v )

    total = get_used_cores(cred_totals, public_cores)

    print "{:->25} {:-<5}".format( '', '' )
    print "{:>25} {:<5}".format( 'total cores configured', public_cores )
    print "{:>25} {:<5}".format( 'total cores in use', total )
    print "{:>25} {:<5}".format( 'total cores available', public_cores - total )
    print "{:->25} {:-<5}".format( '', '' )
    print "{:>25} {:<5}".format( 'total nodes configured', public_nodes )
    print "{:>25} {:<5}".format( 'total nodes free', public_nodes_free )


def print_csv(csv_header_suppress, cred_totals, public_cores, public_nodes, public_nodes_free):
    """
    Display totals to stdout in csv format. Unless --all is used,
    preemptees are not included.
    """

    total = get_used_cores(cred_totals, public_cores)

    # Header
    if not csv_header_suppress:
        csv.writer(sys.stdout).writerow(['total_public_cores', 'free_public_cores',
            'total_public_nodes', 'free_public_nodes'])
    csv.writer(sys.stdout).writerow([str(public_cores), str(public_cores - total),
        public_nodes, public_nodes_free])


def parse_arguments():
    """
    Gather command-line arguments.
    """

    parser = argparse.ArgumentParser(prog='hitparade.py',
        description='Show cluster users and basic usage stats for public ' + \
        'nodes and cores.')
    parser.add_argument( '--debug', '-d', action='store_true', default=False,
        help='Turn on debugging output.')
    parser.add_argument( '--all', '-a', dest='all_jobs', action='store_true', 
        help='Show all core usage.  If set, results will include preemptees',
        default=False )
    parser.add_argument( '--csv', '-c', dest='csv', action='store_true', 
        help='Output core and node totals to csv.',
        default=False )
    parser.add_argument( '--csv-header-suppress', '-s', dest='csv_header_suppress', 
        action='store_true', 
        help='Used with --csv, suppresses header. Default is False, show header.',
        default=False )
    parser.add_argument( '--free-cores', '-f', dest='free_cores', 
        action='store_true', 
        help='Print free cores and exit.',
        default=False )

    return parser.parse_args()

def get_used_cores(cred_totals, public_cores):
    """
    Return used cores.
    """
    total = 0
    for k,v in sorted( cred_totals.items(), key=lambda x: x[1], reverse=True):
        total += v

    return total




if __name__ == '__main__':
    sys.exit(main())
