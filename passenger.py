import random
import pandas as pd
from enum import Enum, auto
import flightschedulegenerator as fsg
import time
import os

class PassengerState(Enum):
    walking = auto()
    waiting = auto()
    boarding = auto()
    checking_in = auto()
    settling = auto()
    boarded = auto()

class Passenger:
    def __init__(self):
        self.df = pd.read_csv("data/passengers.csv")
        self.probability_list = fsg.ScheduleGenerator().generate_probability_list(self.df,"passenger_id")
        self.active_passengers = pd.DataFrame()
    def assign_passenger_info(self):
        passenger = random.choice(self.probability_list)
        passenger_data = self.df.loc[self.df["passenger_id"] == passenger].copy()
        passenger_data["state"] = PassengerState.walking
        passenger_data["state_ticks"] = 0
        return passenger_data
    def assign_plane(self):
        self.df = fsg.Schedule.create_schedule()
        self.df.iloc[random.randint]
    def change_state(self, index, new_state):
        self.active_passengers.at[index, "state"] = new_state
        self.active_passengers.at[index, "state_ticks"] = 0
    def update_states(self):
        for index, row in self.active_passengers.iterrows():
            self.active_passengers.at[index, "state_ticks"] += 1
            state = self.active_passengers.at[index, "state"]
            ticks = self.active_passengers.at[index, "state_ticks"]
            if state == PassengerState.walking and ticks >= 5:
                self.change_state(index, PassengerState.checking_in)
            elif state == PassengerState.checking_in and ticks >= 10:
                self.change_state(index, PassengerState.waiting)
            elif state == PassengerState.waiting and ticks >= 20:
                self.change_state(index, PassengerState.boarding)
            elif state == PassengerState.boarding and ticks >= 8:
                self.change_state(index, PassengerState.settling)
            elif state == PassengerState.settling and ticks >= 5:
                self.change_state(index, PassengerState.boarded)
    def add_passenger(self):
        passenger_data = self.assign_passenger_info()
        self.active_passengers = pd.concat([self.active_passengers, passenger_data],ignore_index=True)

passengers = Passenger()

for i in range(10):
    passengers.add_passenger()
for tick in range(50):
    passengers.update_states()

    os.system("cls" if os.name == "nt" else "clear")

    print(
        passengers.active_passengers[
            ["passenger_id", "state", "state_ticks"]
        ]
    )

    time.sleep(1)