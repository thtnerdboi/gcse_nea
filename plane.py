import pandas as pd
class Plane:
    def __init__(self, model, rows, layout, aisles, capacity, boarding_groups, passengers):
        self.model = model
        self.rows = rows
        self.layout = layout
        self.aisles = aisles
        self.capacity = capacity
        self.boarding_groups = boarding_groups
        self.passengers = passengers
    def __str__(self):
        return f"Plane Model: {self.model}, Rows: {self.rows}, Layout: {self.layout}, Aisles: {self.aisles}, Capacity: {self.capacity}, Boarding Groups: {self.boarding_groups}"
class assignment:
    def read_aircraft_data(filename):
        csv = pd.read_csv(filename)
        return csv
    def create_plane_from_csv(filename):
        data = Plane.read_aircraft_data(filename)
        model = data['Model'][0]
        rows = data['Rows'][0]
        layout = data['Layout'][0]
        aisles = data['Aisles'][0]
        capacity = data['Capacity'][0]
        boarding_groups = data['Boarding Groups'][0]
        return Plane(model, rows, layout, aisles, capacity, boarding_groups)
#plane = Plane("Boeing 737", 30, "3-3", 2, 180, 5, 150)
#print(plane)  # Output: Plane Model: Boeing 737, Rows: 30, Layout: 3-3, Aisles: 2, Capacity: 180, Boarding Groups: 5