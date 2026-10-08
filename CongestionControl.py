# constructor parte 1.1
from numpy import bytes


class CongestionControl:
    def __init__(self, MSS: int):
        self.current_state = "slow start"
        self.MSS = MSS
        self.cwnd = MSS
        self.ssthresh = None

    # parte 1.2
    def get_cwnd(self) -> bytes: 
        return self.cwnd.to_bytes()

    # parte 1.3
    def get_MSS_in_cwnd(self) -> int    :
        return self.cwnd // self.MSS

    #parte 1.4
    def event_ack_recieved(self):
        estado = self.current_state
        if estado == "slow start":
            self.cwnd += self.MSS
            if self.cwnd >= self.ssthresh:
                self.current_state = "congestion avoidance"

        elif estado == "congestion avoidance":
            self.cwnd += (1 / self.get_MSS_in_cwnd())   

    #parte 1.5
    def event_timeout(self):
        estado = self.current_state
        if estado == "congestion avoidance" or estado == "slow start": 
            self.ssthresh = self.cwnd // 2
            self.cwnd = self.MSS
            self.current_state = "slow start" # en slow star el estado no cambia

    