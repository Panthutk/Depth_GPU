import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from compareMode import CompareMode
from detailMode import DetailMode


class Menu:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Depth Gpu Comparison")
        self.root.geometry("1000x600")
        self.read_csv()
        self.menu_page()
        self.gpu_menu_histogram()

        self.run()

    def read_csv(self):
        self.df = pd.read_csv('Clean_gpu_specs_v6.csv')

    def menu_page(self):
        self.label = Label(
            self.root, text="DGC", font=("Arial", 50)).grid(row=0, column=0, sticky="nsew")
        self.last_update = Label(
            self.root, text=f'lasted update on {int(max(self.df["releaseYear"]))}', font=("Arial", 10)).grid(row=1, column=0, sticky="nsew")
        self.compare_button = Button(
            self.root, text="Compare Mode").grid(row=2, column=0, sticky="nsew")
        self.detail_button = Button(
            self.root, text="Detail Mode").grid(row=3, column=0, sticky="nsew")

        # configure column
        self.root.columnconfigure(0, weight=1)

        # configure row
        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=3)
        self.root.rowconfigure(3, weight=3)

    def gpu_menu_histogram(self):

        self.df['releaseYear'] = self.df['releaseYear'].replace(0, 'Unknown')

        self.release_year_counts = self.df['releaseYear'].value_counts()

        self.release_year_counts = self.release_year_counts[
            self.release_year_counts.index != 'Unknown']

        self.release_year_counts.index = self.release_year_counts.index.astype(
            float)

        plt.figure(figsize=(10, 6))
        self.release_year_counts.sort_index().plot(
            marker='o', color='orange', linewidth=2)
        plt.title('Graphics Cards by Release Year')
        plt.xlabel('Release Year')
        plt.ylabel('Number of Cards')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def run(self):
        self.root.mainloop()
