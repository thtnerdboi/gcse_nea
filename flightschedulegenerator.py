import random
import pandas as pd
import plane
class ScheduleGenerator:
    def generate_probability_list(self):
        df = plane.assignment.read_aircraft_data("data/aircraft.csv")
        weight_column = "weight"
        aircraft_probability_list = []
        for _, row in df.iterrows():
            aircraft_code = row["aircraft_code"]
            weight = int(row[weight_column])
            aircraft_probability_list.extend([aircraft_code] * weight)
            return aircraft_probability_list


#result = ScheduleGenerator().generate_schedule()

#print(result)

class Schedule:
    def __init__(self):
        self.schedule = []