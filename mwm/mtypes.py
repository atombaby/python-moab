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

        '''
        try:
            self.AWDuration=int(jobdata[ 'AWDuration' ])
        except:
            self.AWDuration=0

        try:
          self.DRMJID=int(jobdata[ 'DRMJID' ])
        except:
          self.DRMJID = 0

        try:
          self.EEDuration=int(jobdata[ 'EEDuration' ])
        except:
          self.EEDuration = 0

        try:
          self.JobID=int(jobdata[ 'JobID' ])
        except:
          self.JobID = 0

        try:
          self.ReqAWDuration=int(jobdata[ 'ReqAWDuration' ])
        except:
          self.ReqAWDuration = 0

        try:
          self.ReqProcs=int(jobdata[ 'ReqProcs' ])
        except:
          self.ReqProcs = 0

        try:
          self.RsvStartTime=int(jobdata[ 'RsvStartTime' ])
        except:
          self.RsvStartTime = 0

        try:
          self.RunPriority=int(jobdata[ 'RunPriority' ])
        except:
          self.RunPriority = 0

        try:
          self.StartPriority=int(jobdata[ 'StartPriority' ])
        except:
          self.StartPriority = 0

        try:
          self.StartTime=int(jobdata[ 'StartTime' ])
        except:
          self.StartTime = 0

        try:
          self.SubmissionTime=int(jobdata[ 'SubmissionTime' ])
        except:
          self.SubmissionTime = 0

        try:
          self.SuspendDuration=int(jobdata[ 'SuspendDuration' ])
        except:
          self.SuspendDuration = 0

        try:
          self.StatPSDed=float([ 'StatPSDed' ])
        except:
          self.StatPSDed = 0.0

        try:
          self.StatPSUtl=float([ 'StatPSUtl' ])
        except:
          self.StatPSUtl = 0.0

        try:
          self.Account=jobdata[ 'Account' ]
        except:
          self.Account = ""
        try:
          self.Class=jobdata[ 'Class' ]
        except:
          self.Class = ""
        try:
          self.Group=jobdata[ 'Group' ]
        except:
          self.Group = ""
        try:
          self.JobName=jobdata[ 'JobName' ]
        except:
          self.JobName = ""
        try:
          self.MasterHost=jobdata[ 'MasterHost' ]
        except:
          self.MasterHost = ""
        try:
          self.PAL=jobdata[ 'PAL' ]
        except:
          self.PAL = ""
        try:
          self.State=jobdata[ 'State' ]
        except:
          self.State = ""
        try:
          self.User=jobdata[ 'User' ]
        except:
          self.User = ""
      '''
        
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
