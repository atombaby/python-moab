class Job: 
    """
                <job
                    AWDuration="446330"
                    Account="matsen_e"
                    Class="any"
                    DRMJID="107020"
                    EEDuration="2"
                    Group="g_crosenth"
                    JobID="107020"
                    JobName="ssearch36"
                    MasterHost="gizmod10"
                    PAL="campus"
                    ReqAWDuration="259200"
                    ReqProcs="1"
                    RsvStartTime="1346434718"
                    RunPriority="14402"
                    StartPriority="14402"
                    StartTime="1346434718"
                    StatPSDed="446307.460000"
                    StatPSUtl="0.000000"
                    State="Running"
                    SubmissionTime="1346434716"
                    SuspendDuration="0"
                    User="crosenth">
                    <par ID="campus" RsvStartTime="1346434718" StartPriority="14402">
                    </par>
                    <par ID="tukwila" StartPriority="14402">
                    </par>
                </job>
    """
    def __init__(self, jobdata={}):
        # Create with any attributes passed in
        # and then correctly type and re-set, setting
        # defaults along the way.

        integer_values = [ 'AWDuration', 'DRMJID', 'EEDuration', 'JobID',
            'ReqAWDuration', 'ReqProcs', 'RsvStartTime', 'RunPriority',
            'StartPriority', 'StartTime', 'SubmissionTime',
            'SuspendDuration', ]
        float_values = [ 'StatPSDed', 'StatPSUtl', ]
        string_values = [ 'Account', 'Class', 'Group', 'JobName',
            'State', 'User', 'MasterHost', 'PAL', ]

        for v in integer_values:
            if jobdata.has_key( v ):
                vars(self)[v] = int( jobdata[v] )
            else:
                vars(self)[v] = 0

        for v in float_values:
            if jobdata.has_key( v ):
                vars(self)[v] = float( jobdata[v] )
            else:
                vars(self)[v] = 0.0

        for v in string_values:
            if jobdata.has_key( v ):
                vars(self)[v] = int( jobdata[v] )
            else:
                vars(self)[v] = ""
class queue:
    pass

class user:
    pass

class rm:
    pass

class account:
    pass

class node:
    pass
