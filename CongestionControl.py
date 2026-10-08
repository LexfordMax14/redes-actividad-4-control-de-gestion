# constructor parte 1.1
from numpy import byte


class CongestionControl:
    def __init__(self, MSS: int):
        self.current_state = "slow start"
        self.MSS = MSS
        self.cwnd = MSS
        self.ssthresh = None

    # parte 1.2
    def get_cwnd(self) -> bytes: 
        return self.cwnd

    # parte 1.3
    def get_MSS_in_cwnd(self) -> int:
        return self.cwnd // self.MSS    

    

    
