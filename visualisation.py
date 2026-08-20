import tkinter as tk
from tkinter import font
import pandas as pd


# ============================================================
# PIXEL / SPLIT-FLAP DISPLAY
# ============================================================

class SplitFlapText(tk.Frame):
    """
    Creates old airport timetable style characters.

    Example:
        08:15

    becomes individual dark character tiles with a line
    through the middle, similar to a mechanical split-flap board.
    """

    def __init__(
        self,
        parent,
        text,
        pixel_font,
        bg="#F5E49A",
        tile_bg="#17130F",
        tile_fg="#F5E49A"
    ):
        super().__init__(parent, bg=bg)

        self.pixel_font = pixel_font
        self.tile_bg = tile_bg
        self.tile_fg = tile_fg

        self.set_text(text)

    def set_text(self, text):

        # Delete old characters if text is changed
        for widget in self.winfo_children():
            widget.destroy()

        for column, character in enumerate(str(text)):

            tile = tk.Frame(
                self,
                bg=self.tile_bg,
                width=25,
                height=34,
                highlightbackground="#502518",
                highlightthickness=2
            )

            tile.grid(
                row=0,
                column=column,
                padx=1
            )

            tile.grid_propagate(False)

            # Character
            label = tk.Label(
                tile,
                text=character,
                bg=self.tile_bg,
                fg=self.tile_fg,
                font=self.pixel_font
            )

            label.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            # Mechanical split line
            split = tk.Frame(
                tile,
                bg="#502518",
                height=2
            )

            split.place(
                relx=0,
                rely=0.5,
                relwidth=1
            )


# ============================================================
# AIRPORT TIMETABLE GUI
# ============================================================

class Visualisation:

    def __init__(self):

        # ----------------------------------------------------
        # COLOUR PALETTE
        # Based on your airport concept art
        # ----------------------------------------------------

        self.CREAM = "#F5E49A"
        self.LIGHT_CREAM = "#FAEDB1"

        self.BROWN = "#8B4B2E"
        self.DARK_BROWN = "#502518"

        self.BLACK = "#0A0908"

        self.GREY = "#A4A5A5"
        self.DARK_GREY = "#727373"

        self.LIME = "#B7F000"

        self.BURGUNDY = "#72002E"
        self.RED = "#B3002D"

    # ========================================================
    # FIND A PIXEL-LOOKING FONT
    # ========================================================

    def get_pixel_font(self, root, size=12):

        available_fonts = set(font.families(root))

        # Try these in order.
        #
        # Fixedsys is particularly useful because it is an
        # old Windows bitmap-style font.

        preferred_fonts = [
            "Fixedsys",
            "Terminal",
            "Perfect DOS VGA 437",
            "Press Start 2P",
            "Pixel Operator",
            "Courier New"
        ]

        selected = "TkFixedFont"

        for font_name in preferred_fonts:

            if font_name in available_fonts:
                selected = font_name
                break

        return (selected, size, "bold")

    # ========================================================
    # MAIN WINDOW
    # ========================================================

    def table_display(self, df):

        self.df = df.copy()

        root = tk.Tk()

        root.title("OCR Airport Departures")

        root.geometry("1100x700")

        root.configure(
            bg=self.GREY
        )

        self.root = root

        # Fonts
        self.pixel_font = self.get_pixel_font(
            root,
            11
        )

        self.pixel_font_large = self.get_pixel_font(
            root,
            20
        )

        self.pixel_font_small = self.get_pixel_font(
            root,
            9
        )

        # ====================================================
        # MAIN AIRPORT BOARD
        # ====================================================

        outside = tk.Frame(
            root,
            bg=self.BLACK,
            padx=6,
            pady=6
        )

        outside.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        brown_border = tk.Frame(
            outside,
            bg=self.BROWN,
            padx=6,
            pady=6
        )

        brown_border.pack(
            fill="both",
            expand=True
        )

        board = tk.Frame(
            brown_border,
            bg=self.CREAM
        )

        board.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # TITLE
        # ====================================================

        header = tk.Frame(
            board,
            bg=self.CREAM
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        title = tk.Label(
            header,
            text="> OCR AIRPORT DEPARTURES",
            bg=self.CREAM,
            fg=self.DARK_BROWN,
            font=self.pixel_font_large
        )

        title.pack(
            side="left"
        )

        live = tk.Label(
            header,
            text=" LIVE ",
            bg=self.LIME,
            fg=self.BLACK,
            font=self.pixel_font,
            padx=8,
            pady=5,
            highlightbackground=self.BLACK,
            highlightthickness=3
        )

        live.pack(
            side="right"
        )

        # Brown divider
        divider = tk.Frame(
            board,
            height=5,
            bg=self.BROWN
        )

        divider.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )

        # ====================================================
        # SEARCH BAR
        # ====================================================

        controls = tk.Frame(
            board,
            bg=self.CREAM
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        search_label = tk.Label(
            controls,
            text="DESTINATION:",
            bg=self.CREAM,
            fg=self.DARK_BROWN,
            font=self.pixel_font
        )

        search_label.pack(
            side="left",
            padx=(0, 8)
        )

        self.search_entry = tk.Entry(
            controls,
            font=self.pixel_font,
            bg=self.LIGHT_CREAM,
            fg=self.BLACK,
            insertbackground=self.BLACK,
            relief="flat",
            highlightbackground=self.DARK_BROWN,
            highlightthickness=3
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7
        )

        search_button = tk.Button(
            controls,
            text="SEARCH",
            command=self.search,
            font=self.pixel_font_small,
            bg=self.LIME,
            fg=self.BLACK,
            activebackground=self.LIME,
            relief="raised",
            bd=4,
            padx=10,
            pady=5
        )

        search_button.pack(
            side="left",
            padx=(10, 5)
        )

        reset_button = tk.Button(
            controls,
            text="RESET",
            command=self.reset,
            font=self.pixel_font_small,
            bg=self.GREY,
            fg=self.BLACK,
            relief="raised",
            bd=4,
            padx=10,
            pady=5
        )

        reset_button.pack(
            side="left",
            padx=5
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search()
        )

        # ====================================================
        # TIMETABLE AREA
        # ====================================================

        table_container = tk.Frame(
            board,
            bg=self.DARK_BROWN
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # Canvas lets us scroll the timetable
        self.canvas = tk.Canvas(
            table_container,
            bg=self.CREAM,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.rows_frame = tk.Frame(
            self.canvas,
            bg=self.CREAM
        )

        self.rows_frame.bind(
            "<Configure>",
            lambda event:
            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.rows_frame,
            anchor="nw"
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_table
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Add column headers once
        self.create_headers()

        # Fill timetable from pandas DataFrame
        self.fill_table(self.df)

        root.mainloop()

    # ========================================================
    # RESPONSIVE WIDTH
    # ========================================================

    def resize_table(self, event):

        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    # ========================================================
    # COLUMN HEADERS
    # ========================================================

    def create_headers(self):

        headers = [
            ("FLIGHT", 0),
            ("TIME", 1),
            ("DESTINATION", 2),
            ("AIRCRAFT", 3),
            ("DURATION", 4),
            ("STATUS", 5)
        ]

        for text, column in headers:

            header = tk.Label(
                self.rows_frame,
                text=text,
                bg=self.BROWN,
                fg=self.LIGHT_CREAM,
                font=self.pixel_font,
                padx=8,
                pady=10,
                highlightbackground=self.BLACK,
                highlightthickness=2
            )

            header.grid(
                row=0,
                column=column,
                sticky="nsew"
            )

        # Destination gets more room
        self.rows_frame.columnconfigure(
            0,
            weight=1
        )

        self.rows_frame.columnconfigure(
            1,
            weight=1
        )

        self.rows_frame.columnconfigure(
            2,
            weight=4
        )

        self.rows_frame.columnconfigure(
            3,
            weight=2
        )

        self.rows_frame.columnconfigure(
            4,
            weight=2
        )

        self.rows_frame.columnconfigure(
            5,
            weight=2
        )

    # ========================================================
    # CREATE TABLE FROM DATAFRAME
    # ========================================================

    def fill_table(self, dataframe):

        # Remove old rows but KEEP the header row
        for widget in self.rows_frame.winfo_children():

            info = widget.grid_info()

            if info and int(info["row"]) > 0:
                widget.destroy()

        for index, (_, row) in enumerate(
            dataframe.iterrows(),
            start=1
        ):

            # Alternating cream colours
            if index % 2 == 0:
                row_colour = self.CREAM
            else:
                row_colour = self.LIGHT_CREAM

            # ------------------------------------------------
            # FLIGHT NUMBER
            # ------------------------------------------------

            flight = tk.Label(
                self.rows_frame,
                text=row["route_id"],
                bg=row_colour,
                fg=self.DARK_BROWN,
                font=self.pixel_font,
                padx=8,
                pady=12,
                highlightbackground=self.DARK_BROWN,
                highlightthickness=1
            )

            flight.grid(
                row=index,
                column=0,
                sticky="nsew"
            )

            # ------------------------------------------------
            # OLD AIRPORT SPLIT-FLAP TIME
            # ------------------------------------------------

            # Your dataframe currently does not generate times,
            # so this produces example departure times.
            #
            # Once you add departure_time to your DataFrame,
            # replace this section with:
            #
            # departure = row["departure_time"]

            hour = 6 + ((index - 1) // 4)

            minute_options = [
                "00",
                "15",
                "30",
                "45"
            ]

            minute = minute_options[
                (index - 1) % 4
            ]

            departure = f"{hour:02d}:{minute}"

            time_container = tk.Frame(
                self.rows_frame,
                bg=row_colour,
                highlightbackground=self.DARK_BROWN,
                highlightthickness=1
            )

            time_container.grid(
                row=index,
                column=1,
                sticky="nsew"
            )

            split_time = SplitFlapText(
                time_container,
                departure,
                self.pixel_font_small,
                bg=row_colour,
                tile_bg=self.BLACK,
                tile_fg=self.CREAM
            )

            split_time.pack(
                expand=True,
                padx=7,
                pady=5
            )

            # ------------------------------------------------
            # DESTINATION
            # ------------------------------------------------

            destination = tk.Label(
                self.rows_frame,
                text=row["destination"].upper(),
                bg=row_colour,
                fg=self.BLACK,
                font=self.pixel_font,
                anchor="w",
                padx=10,
                highlightbackground=self.DARK_BROWN,
                highlightthickness=1
            )

            destination.grid(
                row=index,
                column=2,
                sticky="nsew"
            )

            # ------------------------------------------------
            # AIRCRAFT
            # ------------------------------------------------

            aircraft = tk.Label(
                self.rows_frame,
                text=row["aircraft_code"],
                bg=row_colour,
                fg=self.BLACK,
                font=self.pixel_font_small,
                highlightbackground=self.DARK_BROWN,
                highlightthickness=1
            )

            aircraft.grid(
                row=index,
                column=3,
                sticky="nsew"
            )

            # ------------------------------------------------
            # FLIGHT DURATION
            # ------------------------------------------------

            minutes = int(
                row["flight_time_min"]
            )

            hours = minutes // 60
            remaining_minutes = minutes % 60

            if hours > 0:

                duration_text = (
                    f"{hours}H "
                    f"{remaining_minutes:02d}M"
                )

            else:

                duration_text = (
                    f"{remaining_minutes}M"
                )

            duration = tk.Label(
                self.rows_frame,
                text=duration_text,
                bg=row_colour,
                fg=self.BLACK,
                font=self.pixel_font_small,
                highlightbackground=self.DARK_BROWN,
                highlightthickness=1
            )

            duration.grid(
                row=index,
                column=4,
                sticky="nsew"
            )

            # ------------------------------------------------
            # STATUS
            # ------------------------------------------------

            status_text, status_colour = (
                self.get_status(index)
            )

            status_container = tk.Frame(
                self.rows_frame,
                bg=row_colour,
                highlightbackground=self.DARK_BROWN,
                highlightthickness=1
            )

            status_container.grid(
                row=index,
                column=5,
                sticky="nsew"
            )

            status = tk.Label(
                status_container,
                text=status_text,
                bg=status_colour,
                fg=(
                    self.LIGHT_CREAM
                    if status_colour == self.BURGUNDY
                    else self.BLACK
                ),
                font=self.pixel_font_small,
                padx=7,
                pady=5,
                highlightbackground=self.BLACK,
                highlightthickness=2
            )

            status.pack(
                expand=True,
                padx=6,
                pady=6
            )

    # ========================================================
    # EXAMPLE FLIGHT STATUS
    # ========================================================

    def get_status(self, row_number):

        statuses = [
            ("ON TIME", self.LIME),
            ("BOARDING", self.BROWN),
            ("GATE 12", self.GREY),
            ("ON TIME", self.LIME),
            ("DELAYED", self.BURGUNDY)
        ]

        return statuses[
            (row_number - 1) % len(statuses)
        ]

    # ========================================================
    # SEARCH USING PANDAS
    # ========================================================

    def search(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        filtered_df = self.df[
            self.df["destination"]
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
        ]

        self.fill_table(
            filtered_df
        )

    # ========================================================
    # RESET SEARCH
    # ========================================================

    def reset(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.fill_table(
            self.df
        )