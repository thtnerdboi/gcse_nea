import random
import pandas as pd
from plane import assignment
class ScheduleGenerator:
    def __init__(self):
        self.aircraft_probability_list = self.generate_probability_list()
        self.df2 = assignment.read_aircraft_data("data/routes.csv")
    def generate_probability_list(self):
        self.df = assignment.read_aircraft_data("data/aircraft.csv")
        weight_column = "weight"
        aircraft_probability_list = []
        for _, row in self.df.iterrows():
            aircraft_code = row["aircraft_code"]
            weight = int(row[weight_column])
            aircraft_probability_list.extend([aircraft_code] * weight)
        return aircraft_probability_list
    def give_plane(self):
        chosen_plane = random.choice(self.aircraft_probability_list)
        return chosen_plane
    def get_flight_no(self, aircraft_code):
        matching_routes = self.df2[self.df2["aircraft_code"] == aircraft_code]
        chosen_route = matching_routes.sample(n=1)
        return chosen_route



#result = ScheduleGenerator().generate_probability_list()
#print(result)

class Schedule:
    def __init__(self):
        self.df = pd.DataFrame(
            columns=[
                "flight_number",
                "departure_time",
                "arrival_time",
                "origin",
                "destination",
                "aircraft_code",
                "flight_time_min"
            ]
        )

    def create_schedule(self):
        selected_routes = []
        generator = ScheduleGenerator()
        for i in range(121):
            aircraft_code = generator.give_plane()
            chosen_route = generator.get_flight_no(aircraft_code)
            if chosen_route is not None:
                selected_routes.append(chosen_route)
        if selected_routes:
            self.df = pd.concat(selected_routes,ignore_index=True)
        return self.df
#chosen_plane = ScheduleGenerator().give_plane()
#print(chosen_plane) 
#schedule = Schedule()
#print(schedule.df)
#flight_number = ScheduleGenerator().get_flight_no(chosen_plane)
#print(flight_number)

print(Schedule().create_schedule())