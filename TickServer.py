import zmq
import math
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5555')
# socket.bind('tcp://localhost:5555') for running on Windows, maybe

class InstrumentPrice():
    def __init__(self):
        self.symbol = 'SYMBOL'
        self.t = time.time()
        self.value = 100.
        self.sigma = 0.4
        self.r = 0.01
        
    def simulate_value(self):
        t = time.time()
        # dt in trading year fraction
        dt = (t - self.t) / (252 * 8  * 60 * 60)
        dt *= 500
        self.t = t
        
        self.value *= math.exp((self.r - 0.5 * self.sigma ** 2) * dt + self.sigma * math.sqrt(dt) * random.gauss(0, 1))
        return self.value
        

ip = InstrumentPrice()

while True:
    msg = f'{ip.symbol} {ip.simulate_value():.2f}'
    print(msg)
    socket.send_string(msg)
    time.sleep(random.random() * 2)