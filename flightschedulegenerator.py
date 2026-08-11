import random
import pandas as pd
from plane import assignment
class ScheduleGenerator:
    def __init__(self):
        aircraft_df = assignment.read_aircraft_data("data/aircraft.csv")
        self.aircraft_probability_list = self.generate_probability_list(aircraft_df,"aircraft_code")
        self.df2 = assignment.read_aircraft_data("data/routes.csv")
    def generate_probability_list(self, df, data_point):
        weight_column = "weight"
        probability_list = []
        for _, row in df.iterrows():
            code = row[data_point]
            weight = int(row[weight_column])
            probability_list.extend([code] * weight)
        return probability_list
    def give_plane(self):
        chosen_plane = random.choice(self.aircraft_probability_list)
        return chosen_plane
    def get_flight_no(self, aircraft_code):
        matching_routes = self.df2[self.df2["aircraft_code"] == aircraft_code]
        route_probability_list = self.generate_probability_list(matching_routes,"route_id")
        chosen_route = random.choice(route_probability_list)
        chosen_route = matching_routes[matching_routes["route_id"] == chosen_route]
        #Debug statements below to test aspects of the method
        #print("Aircraft:", aircraft_code)
        #print("Matching routes:")
        #print(matching_routes)
        #print("Chosen route id:", chosen_route)
        #print("Chosen route:")
        #print(chosen_route)
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
chosen_plane = ScheduleGenerator().give_plane()
print(chosen_plane) 
schedule = Schedule()
print(schedule.df)
flight_number = ScheduleGenerator().get_flight_no(chosen_plane)
print(flight_number)
Schedule1 = Schedule()
print(Schedule1.create_schedule())