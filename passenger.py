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
    boarded = auto()
    #Automatically creates integer values for the order of each state

class Passenger:
    def __init__(self):
        self.df = pd.read_csv("data/passengers.csv")#Creates passengers dataframe from passengers.csv
        self.probability_list = fsg.ScheduleGenerator().generate_probability_list(self.df,"passenger_id")# Generates probability list of passengers based on weights
        self.active_passengers = pd.DataFrame()#Generates empty df for the active passengers
        self.schedule = fsg.Schedule().create_schedule()
        self.pending_passengers = pd.DataFrame()
    def assign_passenger_info(self):
        passenger = random.choice(self.probability_list) # Choses random passenger from the list
        passenger_data = self.df.loc[self.df["passenger_id"] == passenger].copy()# Fetches all passenger data using the name found from the csv
        passenger_data["state"] = PassengerState.walking #Sets passenger state as walking to start with
        passenger_data["state_ticks"] = 0#Starts at 0 to increment every tick
        return passenger_data
    def assign_plane(self,passenger_data):
        random_index = random.randint(0, len(self.schedule) - 1)
        flight = self.schedule.iloc[random_index]#Accidentally wrote light instead of flight and broke my whole code
        passenger_data["flight"] = flight["route_id"]
        passenger_data["destination"] = flight["destination"]
        passenger_data["departure_time"] = flight["departure_time"]
        return passenger_data
        # It's in the name ngl
    def change_state(self, index, new_state):
        self.active_passengers.at[index, "state"] = new_state
        self.active_passengers.at[index, "state_ticks"] = 0
        #Changes state what else is there to say
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
            #Bunch of conditionals for when to change passenger state
    def add_passenger(self):
        passenger_data = self.assign_passenger_info()#Assigns info
        passenger_data = self.assign_plane(passenger_data)#Assigns plane
        passenger_data = self.assign_arrival_time(passenger_data)
        self.pending_passengers = pd.concat([self.pending_passengers,passenger_data],ignore_index=True)#Adds passenger to the empty df made earlier(See it is useful)
        #Assigns everything then adds to the empty df I made before ngl there's not much to it
    def check_arrivals(self, current_time):
        if self.pending_passengers.empty:
            return
        arriving = self.pending_passengers[self.pending_passengers["arrival_time"] <= current_time]
        if not arriving.empty:
            self.active_passengers = pd.concat([self.active_passengers,arriving],ignore_index=True)
            self.pending_passengers = (self.pending_passengers[self.pending_passengers["arrival_time"] > current_time])
    def time_to_minutes(self, time_string):
        hours, minutes = map(int, time_string.split(":"))
        return hours * 60 + minutes
    def assign_arrival_time(self, passenger_data):
        departure_time = passenger_data["departure_time"].iloc[0]
        departure_minutes = self.time_to_minutes(departure_time)
        passenger_data["arrival_time"] = (departure_minutes - random.randint(90, 180))
        return passenger_data
