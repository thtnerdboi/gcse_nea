import random
import pandas as pd
import plane
class ScheduleGenerator:
    def generate_probability_list(self):
        self.df = plane.assignment.read_aircraft_data("data/aircraft.csv")
        weight_column = "weight"
        aircraft_probability_list = []
        for _, row in self.df.iterrows():
            aircraft_code = row["aircraft_code"]
            weight = int(row[weight_column])
            aircraft_probability_list.extend([aircraft_code] * weight)
        return aircraft_probability_list
    def give_plane(self):
        aircraft_probability_list = self.generate_probability_list()
        chosen_plane = random.choice(aircraft_probability_list)
        return chosen_plane
    def get_flight_no(self, aircraft_code):
        df = plane.assignment.read_aircraft_data("data/routes.csv")
        matching_routes = df[df["aircraft_code"] == aircraft_code]
        chosen_route = matching_routes.sample(n=1)
        return chosen_route



#result = ScheduleGenerator().generate_probability_list()
#print(result)

class Schedule:
    def __init__(self):
        self.df = pd.DataFrame(columns=["flight_number", "departure_time", "arrival_time", "origin", "destination", "aircraft_code", "flight_time_min"])
        for i in range(121):
            self.df.loc[i, "aircraft_code"] = ScheduleGenerator().give_plane()
            self.df.loc[i, "origin"] = "London Heathrow Airport(LHR)"
            #self.df.loc[i, "departure_time"] = pd.Timestamp.now() + pd.Timedelta(minutes=self.df.loc['flight_time'])
            #self.df.loc[i, "flight_number"] = 
chosen_plane = ScheduleGenerator().give_plane()
print(chosen_plane) 
schedule = Schedule()
print(schedule.df)
flight_details = ScheduleGenerator().get_flight_no("A320")
print(flight_details)