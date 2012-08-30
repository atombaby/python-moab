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
        self.connect_command = [ 'mdiag', '--xml' ]

        try:
            self.hostname = hostname
            self.connect_command.append( '--host=' + self.hostname )
        except NameError:
            pass
        try:
            self.loglevel = loglevel
            self.connect_command.append(
                '--loglevel=' + str( self.loglevel )
            )
        except NameError:
            pass
        try:
            self.port = port
            self.connect_command.append( '--port=' + str( self.port ) )
        except NameError:
            pass
        try:
            self.timeout = timeout
            self.connect_command.append(
                '--timeout=' + str( self.timeout )
            )
        except NameError:
            pass

    def getRMData( self ):
        command = [ '-R' ]
        xml_data = self.doCommand( command )
        print xml_data

    def doCommand( self, command ):
        return subprocess.check_output( self.connect_command + command )


# internal functions & classes

def main():
        # bar = Scheduler(hostname='bar', port=5309, timeout=12, loglevel=1)
        bar = Scheduler( )
        bar.getRMData()

if __name__ == '__main__':
        status = main()
        sys.exit(status)
