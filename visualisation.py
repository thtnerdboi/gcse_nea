import pandas as pd
import tkinter as tk
from tkinter import ttk
import pygame as pg
import flightschedulegenerator as fsg
import passenger
import simulation

class Visualisation:

    def full_display(self, df, simulation):
        root = tk.Tk()
        root.title("OCR Airport Simulation")
        root.geometry("1400x600")

        left_frame = tk.Frame(root)
        left_frame.pack(side="left", fill="both", expand=True)

        right_frame = tk.Frame(root)
        right_frame.pack(side="right", fill="both", expand=True)
        schedule_tree = ttk.Treeview(left_frame,
            columns=("flight", "destination", "aircraft", "duration", "departs"),
            show="headings")

        schedule_tree.heading("flight", text="Route")
        schedule_tree.heading("destination", text="Destination")
        schedule_tree.heading("aircraft", text="Aircraft")
        schedule_tree.heading("duration", text="Flight Time")
        schedule_tree.heading("departs", text="Departure Time")
        for _, row in df.iterrows():
            schedule_tree.insert(
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

        schedule_tree.pack(fill="both", expand=True)
        time_label = tk.Label(
            right_frame,
            text="Time: 00:00",
            font=("Arial", 16)
        )
        time_label.pack()

        passenger_tree = ttk.Treeview(
            right_frame,
            columns=("passenger", "flight", "departure", "state"),
            show="headings"
        )

        passenger_tree.heading("passenger", text="Passenger")
        passenger_tree.heading("flight", text="Flight")
        passenger_tree.heading("departure", text="Departure")
        passenger_tree.heading("state", text="State")

        passenger_tree.pack(fill="both", expand=True)

        def update():
            simulation.update()

            hours = simulation.current_time // 60
            minutes = simulation.current_time % 60

            time_label.config(
                text=f"Time: {hours:02d}:{minutes:02d}"
            )

            passenger_tree.delete(*passenger_tree.get_children())

            for _, row in simulation.passengers.active_passengers.iterrows():
                passenger_tree.insert(
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