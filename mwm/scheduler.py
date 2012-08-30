"""Functions for interacting with the MWM scheduler"""

import sys
import subprocess
import elementtree.ElementTree as et

# constants
# exception classes
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
        return subprocess.check_output( command )


# internal functions & classes

def main():
        # bar = Scheduler(hostname='bar', port=5309, timeout=12, loglevel=1)
        bar = Scheduler( )
        print bar.getRMData()['STATE']
        print bar.getSchedData()['iteration']

if __name__ == '__main__':
        status = main()
        sys.exit(status)
