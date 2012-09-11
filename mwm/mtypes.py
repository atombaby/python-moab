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
            # (node, cores on node)
            vars(self)[d] = []
            try:
                elem = data[d].split(',')
                for alloc in elem:
                    alloc = tuple( alloc.split( ':' ) )
                    vars(self)[d].append( alloc )
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
            ( 'LastChargeTime',  'int' ),
            ( 'Name',            'string' ),
            ( 'Partition',       'string' ),
            ( 'Priority',        'int' ),
            ( 'Resources',       'string' ),
            ( 'RsvGroup',        'string' ),
            ( 'StatCAPS',        'float' ),
            ( 'StatCIPS',        'float' ),
            ( 'StatTAPS',        'float' ),
            ( 'StatTIPS',        'float' ),
            ( 'SubType',         'string' ),
            ( 'Type',            'string' ),
            ( 'cost',            'float' ),
            ( 'ctime',           'int' ),
            ( 'duration',        'int' ),
            ( 'endtime',         'int' ),
            ( 'flags',           'list' ),
            ( 'starttime',       'int' ),
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
    pass
