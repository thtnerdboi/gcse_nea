import os
import time
from passenger import Passenger
class Simulation:
    def __init__(self):
        self.passengers = Passenger()
        self.current_time = 0
    def setup(self, number_of_passengers):
        for i in range(number_of_passengers):
            self.passengers.add_passenger()
    def update(self):
        self.passengers.check_arrivals(self.current_time)
        self.passengers.update_states()
        self.current_time += 1