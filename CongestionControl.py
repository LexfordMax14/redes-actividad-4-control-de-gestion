# constructor parte 1.1
from numpy import byte


class CongestionControl:
    def __init__(self, MSS: int):
        self.current_state = "slow start"
        self.MSS = MSS
        self.cwnd = MSS
        self.ssthresh = None

    def get_cwnd(self): bytes 

    
