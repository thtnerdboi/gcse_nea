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

simulation = Simulation()

simulation.setup(100)

for tick in range(1440):
    simulation.update()

    os.system(
        "cls" if os.name == "nt" else "clear"
    )

    print("TIME:", simulation.current_time)

    print(
        simulation.passengers.active_passengers[
            [
                "passenger_id",
                "flight",
                "departure_time",
                "state",
                "state_ticks"
            ]
        ]
    )

    time.sleep(0.1)