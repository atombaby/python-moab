def _process( self, data={}, attrs=[] ):
    for d, t in attrs:
        if t == 'int':
            vars(self)[d] = 0
            try:
                vars(self)[d] = int( data[d] )
            except KeyError:
                vars(self)[d] = 0
            except ValueError:
                print "invalid data \"{}\" for \"{}\"".format(
                    t, data[d] )

        elif t == 'float':
            vars(self)[d] = 0.0
            try:
                vars(self)[d] = float( data[d] )
            except KeyError:
                vars(self)[d] = 0.0
            except ValueError:
                print "invalid data \"{}\" for \"{}\"".format(
                    d, data[d] )

        elif t == 'string':
            vars(self)[d] = ""
            try:
                vars(self)[d] = data[d]
            except KeyError:
                vars(self)[d] = ""

        elif t == 'nodelist':
            # {node:cores on node}
            vars(self)[d] = {}
            try:
                for alloc in data[d].split(','):
                    try:
                        nn, cores = alloc.split( ':' )
                        vars(self)[d][nn] = int( cores )
                    except ValueError:
                        # If there isn't a processor specification
                        # after the node name, then only a single
                        # processor is assigned
                        nn = alloc
                        vars(self)[d][nn] = 1
            except KeyError:
                vars(self)[d] = []

        elif t == 'list':
            vars(self)[d] = []
            try:
                vars(self)[d] = data[d].split(',')
            except KeyError:
                vars(self)[d] = []

class Job: 
    def __init__(self, rawdata={}):
        # Create with any attributes passed in
        # and then correctly type and re-set, setting
        # defaults along the way.

        attributes = [
            ( 'AWDuration', 'int' ),
            ( 'DRMJID', 'int' ),
            ( 'EEDuration', 'int' ),
            ( 'JobID', 'int' ),
            ( 'NCReqMin', 'int' ),
            ( 'ReqAWDuration', 'int' ),
            ( 'ReqProcs', 'int' ),
            ( 'RsvStartTime', 'int' ),
            ( 'RunPriority', 'int' ),
            ( 'StartCount', 'int' ),
            ( 'StartPriority', 'int' ),
            ( 'StartTime', 'int' ),
            ( 'SubmissionTime', 'int' ),
            ( 'SuspendDuration', 'int' ),
            ( 'UMask', 'int' ),
            ( 'StatPSDed', 'float' ),
            ( 'StatPSUtl', 'float' ),
            ( 'StatMSUtl', 'float' ),
            ( 'Account', 'string' ),
            ( 'AllocNodeList', 'nodelist' ),
            ( 'AllocPartition', 'string' ),
            ( 'BlockReason', 'string' ),
            ( 'Class', 'string' ),
            ( 'EffPAL', 'string' ),
            ( 'EState', 'string' ),
            ( 'Flags', 'string' ),
            ( 'Group', 'string' ),
            ( 'ID', 'string' ),
            ( 'IWD', 'string' ),
            ( 'JobName', 'string' ),
            ( 'MasterHost', 'string' ),
            ( 'NodeAccess', 'string' ),
            ( 'PAL', 'string' ),
            ( 'QueueStatus', 'string' ),
            ( 'ReqNodeMem', 'string' ),
            ( 'ReqNodeProc', 'string' ),
            ( 'ReqNodeSwap', 'string' ),
            ( 'ReqPartition', 'string' ),
            ( 'ReqProcPerTask', 'string' ),
            ( 'RM', 'string' ),
            ( 'State', 'string' ),
            ( 'TCReqMin', 'string' ),
            ( 'User', 'string' ),
        ]

        _process( self, data=rawdata, attrs=attributes )


class Queue:
    pass

class Reservation:
    def __init__(self, rawdata={}):
        attributes=[
            ( 'AllocNodeCount',  'int' ),
            ( 'AllocNodeList',   'list' ),
            ( 'AllocProcCount',  'int' ),
            ( 'AllocTaskCount',  'int' ),
            ( 'cost',            'float' ),
            ( 'ctime',           'int' ),
            ( 'duration',        'int' ),
            ( 'endtime',         'int' ),
            ( 'flags',           'list' ),
            ( 'HostExp',         'string' ),
            ( 'LastChargeTime',  'int' ),
            ( 'Name',            'string' ),
            ( 'Partition',       'string' ),
            ( 'Priority',        'int' ),
            ( 'ReqNodeList',     'nodelist' ),
            ( 'Resources',       'string' ),
            ( 'RsvGroup',        'string' ),
            ( 'RsvParent',       'string' ),
            ( 'starttime',       'int' ),
            ( 'StatCAPS',        'float' ),
            ( 'StatCIPS',        'float' ),
            ( 'StatTAPS',        'float' ),
            ( 'StatTIPS',        'float' ),
            ( 'SubType',         'string' ),
            ( 'Type',            'string' ),
        ]
        _process( self, rawdata, attributes)


class User:
    def __init__(self, rawdata={}):
        attributes=[
            ( 'ADEF', 'string' ),
            ( 'ALIST', 'string' ),
            ( 'ENABLEPROFILING', 'string' ),
            ( 'ID', 'string' ),
            ( 'ROLE', 'string' ),
        ]
        _process( self, rawdata, attributes)

class ResourceManager:
    pass

class Account:
    pass

class Node:
    def __init__(self, rawdata={}):
        attributes=[
            ( 'ARCH',               'string'),
            ( 'AVLCLASS',           'string'),
            ( 'CFGCLASS',           'string'),
            ( 'FEATURES',           'list'	),
            ( 'LASTUPDATETIME',     'int'	),
            ( 'MAXJOB',             'int'	),
            ( 'MAXJOBPERUSER',      'int'	),
            ( 'MAXLOAD',            'float'	),
            ( 'NODEID',             'string'),
            ( 'NODEINDEX',          'int'	),
            ( 'NODESTATE',          'string'),
            ( 'OS',                 'string'),
            ( 'OSLIST',             'string'),
            ( 'PARTITION',          'string'),
            ( 'PRIORITY',           'int'	),
            ( 'PROCSPEED',          'int'	),
            ( 'RADISK',             'int'	),
            ( 'RAMEM',              'int'	),
            ( 'RAPROC',             'int'	),
            ( 'RASWAP',             'int'	),
            ( 'RCDISK',             'int'	),
            ( 'RCMEM',              'int'	),
            ( 'RCPROC',             'int'	),
            ( 'RESCOUNT',           'int'	),
            ( 'RMACCESSLIST',       'string'),
            ( 'RSVLIST',            'list'	),
            ( 'SPEED',              'float'	),
            ( 'STATACTIVETIME',     'int'	),
            ( 'STATMODIFYTIME',     'int'	),
            ( 'STATTOTALTIME',      'int'	),
            ( 'STATUPTIME',         'int'	),
        ]
        _process( self, rawdata, attributes )

    pass
