# constructor parte 1.1


class CongestionControl:
    def __init__(self, MSS: int):
        self.current_state = "slow start"
        self.MSS = MSS
        self.cwnd = MSS
        self.ssthresh = None

    # parte 1.2
    def get_cwnd(self) -> int:
        return int(self.cwnd)

    # parte 1.3
    def get_MSS_in_cwnd(self) -> int    :
        return int(self.cwnd // self.MSS)

    #parte 1.4
    def event_ack_received(self):
        estado = self.current_state
        if estado == "slow start":
            self.cwnd += self.MSS
            if self.ssthresh is not None and self.cwnd >= self.ssthresh:
                self.current_state = "congestion avoidance"

        elif estado == "congestion avoidance":
            self.cwnd += self.MSS / self.get_MSS_in_cwnd()

    #parte 1.5
    def event_timeout(self):
        estado = self.current_state
        if estado == "congestion avoidance" or estado == "slow start": 
            self.ssthresh = int(self.cwnd // 2)
            self.cwnd = self.MSS
            self.current_state = "slow start" # en slow star el estado no cambia

    #parte 1.6 
    def is_state_slow_start(self) -> bool:
        return self.current_state == "slow start"

    def is_state_congestion_avoidance(self) -> bool:
        return self.current_state == "congestion avoidance"

    def get_ssthresh(self) -> int | None:
        return self.ssthresh

    
