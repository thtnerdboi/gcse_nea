from tabulate import tabulate
import random
import pandas as pd
import tkinter as tk
from tkinter import ttk
from plane import assignment
class ScheduleGenerator:
    def __init__(self):
        aircraft_df = assignment.read_aircraft_data("data/aircraft.csv") # Creates dataframe from aircraft.csv
        self.aircraft_probability_list = self.generate_probability_list(aircraft_df,"aircraft_code")# Creates probability list calling on below method
        self.df2 = assignment.read_aircraft_data("data/routes.csv") #Creates another dataframe from routes.csv allowing the selected plane to get the selectedpi 
    def generate_probability_list(self, df, data_point):
        weight_column = "weight" #Calls weight column
        probability_list = [] # Creates empty list to append to for the weighted probabilities
        for _, row in df.iterrows():
            code = row[data_point]#Finds code
            weight = int(row[weight_column]) #Find probability wieghts
            probability_list.extend([code] * weight) #Adds code to probability list at the number of times of the weight
        return probability_list
    def give_plane(self):
        chosen_plane = random.choice(self.aircraft_probability_list)#Selects randomly from the probability list to get an aircraft
        return chosen_plane
    def get_flight_no(self, aircraft_code):
        matching_routes = self.df2[self.df2["aircraft_code"] == aircraft_code]# Finds matching routes that use the selected plane
        route_probability_list = self.generate_probability_list(matching_routes,"route_id") # Generates probability list for routes
        chosen_route = random.choice(route_probability_list)#Choses a route from the list
        chosen_route = matching_routes[matching_routes["route_id"] == chosen_route] #Grabs the full data of the route from the csv
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
        )# Creates empty dataframe with columns to be appended

    def create_schedule(self):
        selected_routes = []# Creates empty list for the selected routes
        generator = ScheduleGenerator()# Constructor for the generator object
        for i in range(121):
            aircraft_code = generator.give_plane() # Gets aircraft model/code from get_plane() method
            chosen_route = generator.get_flight_no(aircraft_code)# Uses aircraft code to get a route that matches with the plane
            if chosen_route is not None:
                selected_routes.append(chosen_route)# Appends route to selected routes list
        if selected_routes:
            self.df = pd.concat(selected_routes,ignore_index=True)#Concatenates dataframe
        self.df = self.df.loc[~self.df.eq(self.df.shift()).all(axis=1)]# Deletes consecutively duplicate routes
        self.df = self.df.drop(columns = ["weight"])# Drops weight column from timetable(Weight was only for the probabilities of the route's selection not for the user to see)
        return self.df
#Testing below
chosen_plane = ScheduleGenerator().give_plane()
print(chosen_plane) 
schedule = Schedule()
print(schedule.df)
flight_number = ScheduleGenerator().get_flight_no(chosen_plane)
print(flight_number)
Schedule1 = Schedule()
df = Schedule1.create_schedule()
print(df)
print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

#TKinter Visualistation
class Visualisation:
    def table_display(self, df):
        root = tk.Tk()
        root.title("OCR Airport Timetable")
        root.geometry("800x500")
        tree = ttk.Treeview(
            root,
            columns=("flight", "destination", "aircraft", "duration"),
            show="headings"
        )
        tree.heading("flight", text="Route")
        tree.heading("destination", text="Destination")
        tree.heading("aircraft", text="Aircraft")
        tree.heading("duration", text="Flight Time")
        for _, row in df.iterrows():
            tree.insert(
                "",
                "end",
                values=(
                    row["route_id"],
                    row["destination"],
                    row["aircraft_code"],
                    row["flight_time_min"]
                )
            )
        tree.pack(fill="both", expand=True)
        root.mainloop()

gui = Visualisation()
gui.table_display(df)