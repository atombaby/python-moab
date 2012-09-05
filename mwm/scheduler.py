#!/usr/bin/env python
"""Functions for interacting with the MWM scheduler"""

import sys
import subprocess
import xml.etree.ElementTree as et

# constants
# exception classes
class MWMConnectError(Exception):
    def __init__( self, message ):
        print "ERROR: " + message
# interface functions
# classes

class Scheduler():
    """ An object holding scheduler information """
    """def __init__(self,
                 hostname=False,
                 loglevel=False,
                 port=False,
                 timeout=False):"""


    def __init__(self):

        self.state = "UNKNOWN"
        self.base_options = [ '--xml' ]

        try:
            self.hostname = hostname
            self.base_options.append( '--host=' + self.hostname )
        except NameError:
            pass
        try:
            self.loglevel = loglevel
            self.base_options.append(
                '--loglevel=' + str( self.loglevel )
            )
        except NameError:
            pass
        try:
            self.port = port
            self.base_options.append( '--port=' + str( self.port ) )
        except NameError:
            pass
        try:
            self.timeout = timeout
            self.base_options.append(
                '--timeout=' + str( self.timeout )
            )
        except NameError:
            pass

        # Make trial connection to scheduler
        command = [ 'mdiag' ]
        options = [ '-S' ]
        r = self.doCommand( command + self.base_options + options )
        xml_data = et.fromstring( r )
        state = xml_data.find( 'sched' ).attrib[ 'STATE' ]

        if state != 'RUNNING':
            print ( 'WARNING: scheduler is '
                   'not \'running\' ( {} )'.format( state ) )

        self.state = state
        self.version = xml_data.find(
            'sched/Version' ).attrib[ 'moabversion' ]

    def getSchedData( self ):
        command = [ 'mschedctl' ]
        options = [ '' ]
        xml_data = et.fromstring( 
            self.doCommand( command + self.base_options + options )
        )

        v = []

        for t in xml_data.findall( 'sched' ):
            v = v + t.items()

        return dict( v )

    def getRMData( self ):
        command = [ 'mdiag' ]
        options = [ '-R' ]
        xml_data = et.fromstring(
            self.doCommand( command + self.base_options + options )
        )

        v = []

        for t in xml_data.findall( 'rm' ):
            v = v + t.items()

        return dict( v )

    def doCommand( self, command ):
        try:
            t = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT
            )
        except OSError:
            raise MWMConnectError( "Moab binaries not found" )
        except subprocess.CalledProcessError, e:
            errdata = et.fromstring( e.output )
            msg = errdata.find( 'Message' ).text
            raise MWMConnectError( "Connection failure: " + msg )
        except:
            raise MWMConnectError(
                "unknown error intiating connection to MWM"
            )
        return t

# internal functions & classes

def main():
        # bar = Scheduler(hostname='bar', port=5309, timeout=12, loglevel=1)
        print "Connecting to default scheduler"
        s = Scheduler( )
        print "found scheduler version {} ". format( s.version )

        print "... getting RM state..."
        retval = s.getRMData()['STATE']
        print retval

if __name__ == '__main__':
        status = main()
        sys.exit(status)
