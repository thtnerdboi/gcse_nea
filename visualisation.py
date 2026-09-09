import pandas as pd
import tkinter as tk
from tkinter import ttk
import pygame as pg
import flightschedulegenerator as fsg
import passenger


class Visualisation:

    def table_display(self, df):

        root = tk.Tk()
        root.title("OCR Airport Timetable")
        root.geometry("800x500")

        tree = ttk.Treeview(
            root,
            columns=("flight", "destination", "aircraft", "duration", "departs"),
            show="headings"
        )

        tree.heading("flight", text="Route")
        tree.heading("destination", text="Destination")
        tree.heading("aircraft", text="Aircraft")
        tree.heading("duration", text="Flight Time")
        tree.heading("departs", text="Departure Time")

        for _, row in df.iterrows():

            tree.insert(
                "",
                "end",
                values=(
                    row["route_id"],
                    row["destination"],
                    row["aircraft_code"],
                    row["flight_time_min"],
                    row["departure_time"]
                )
            )

        tree.pack(fill="both", expand=True)

        root.mainloop()

def passenger_display(self, simulation):
    root = tk.Tk()
    root.title("OCR Airport Passenger Simulation")
    root.geometry("900x500")

    time_label = tk.Label(root, text="Time: 00:00", font=("Arial", 16))
    time_label.pack()

    tree = ttk.Treeview(
        root,
        columns=("passenger", "flight", "departure", "state"),
        show="headings"
    )

    tree.heading("passenger", text="Passenger")
    tree.heading("flight", text="Flight")
    tree.heading("departure", text="Departure")
    tree.heading("state", text="State")

    tree.pack(fill="both", expand=True)

    def update():
        simulation.update()

        hours = simulation.current_time // 60
        minutes = simulation.current_time % 60

        time_label.config(
            text=f"Time: {hours:02d}:{minutes:02d}"
        )

        tree.delete(*tree.get_children())

        for _, row in simulation.passengers.active_passengers.iterrows():
            tree.insert(
                "",
                "end",
                values=(
                    row["passenger_id"],
                    row["flight"],
                    row["departure_time"],
                    row["state"].name
                )
            )

        if simulation.current_time < 1440:
            root.after(100, update)

    update()

    root.mainloop()