import random
import pandas as pd
from enum import Enum, auto
import flightschedulegenerator as fsg

class PassengerState(Enum):
    walking = auto()
    waiting = auto()
    boarding = auto()
    checking_in = auto()
    settling = auto()


class Passenger:
    def __init__(self):
        self.df = pd.read_csv("data/passengers.csv")
        self.probability_list = fsg.ScheduleGenerator.generate_probability_list(self.df, "passenger_id")
    def assign_passenger_info(self):
        passenger = random.choice(self.probability_list)
        passenger_data = self.df.loc[self.df["passenger_id"] == passenger].copy()
        passenger_data["state"] = PassengerState.walking
        return passenger_data
    def assign_plane(self):
        self.df = fsg.Schedule.create_schedule()
        self.df.iloc[random.randint]

    


class Bags:
    def __init__(self, passenger, num_bags, dangerous_items, weight):
        self.passenger = passenger
        self.num_bags = num_bags
        self.dangerous_items = dangerous_items
        self.weight = weight

data = Passenger().assign_passenger_info()
print(data)