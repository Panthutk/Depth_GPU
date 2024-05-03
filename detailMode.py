import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DetailMode:
    def __init__(self, master, df) -> None:
        self.master = master
        self.df = df
        self.master.title("Detail Mode")
        self.master.geometry("1300x800")
        self.setup_head()
        self.setup_head_frame()

        self.run()

    def setup_head(self):
        # Create head frame at the top
        self.head_frame = Frame(self.master, height=90, bg='#989898')
        self.head_frame.pack(fill=X)

    def show_gpu_info_and_graph(self):
        # Create a frame container for the lower part
        self.lower_frame = Frame(self.master)
        self.lower_frame.pack(fill=BOTH, expand=True)

        # Create left frame below head frame
        self.left_frame = Frame(
            self.lower_frame, width=410, height=710, bg='#F3F2F2')
        self.left_frame.pack(side=LEFT, fill=Y)

        # Create right frame which takes the rest of the space
        self.right_frame = Frame(self.lower_frame, bg='white')
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True)

    def setup_head_frame(self):
        # Create the label for the head frame
        self.home = Button(self.head_frame, text="Menu", font=(
            "Arial", 12), bg='#989898', command=self.load_menu_page, width=10, height=2)
        self.home.pack(side=LEFT, padx=20, pady=18)

        # Create the ComboBox for manufacturer
        self.manufacturer_label = Label(
            self.head_frame, text="Manufacturer:", font=("Arial", 12), bg='#989898')
        self.manufacturer_label.pack(side=LEFT, padx=10)

        self.manufacturer_combobox = ttk.Combobox(
            self.head_frame, values=[str(val).strip() for val in self.df['manufacturer'].unique()], font=("Arial", 12), state='readonly')
        self.manufacturer_combobox.pack(side=LEFT)

    def load_menu_page(self):
        # Destroy the current frame and load the menu page
        self.master.destroy()
        from menu import Menu
        Menu()

    def run(self):
        self.master.mainloop()

    def load_menu_page(self):
        # Destroy the current frame and load the menu page
        self.master.destroy()
        from menu import Menu
        Menu()

    def run(self):
        self.master.mainloop()
