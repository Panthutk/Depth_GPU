import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Menu:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Depth GPU Comparison")
        self.root.geometry("1200x600")
        self.read_csv()

        self.setup_frames()
        self.menu_page()
        self.gpu_menu_histogram()

        self.run()

    def read_csv(self):
        self.df = pd.read_csv('Clean_gpu_specs_v6.csv')

    def setup_frames(self):
        self.left_frame = Frame(self.root, width=200, bg='gray')
        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.right_frame = Frame(self.root, width=1000, bg='white')
        self.right_frame.grid(row=0, column=1, sticky="nswe")

        # Configure column and row for frames
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=5)
        self.root.grid_rowconfigure(0, weight=1)

    def menu_page(self):
        Label(self.left_frame, text="DGC", font=(
            "Arial", 24), bg='gray').pack(pady=20)
        Label(self.left_frame, text=f'Last updated: {int(max(self.df["releaseYear"]))}', font=(
            "Arial", 10), bg='gray').pack(pady=10)
        Button(self.left_frame, text="Compare Mode").pack(fill='x', pady=10)
        Button(self.left_frame, text="Detail Mode").pack(fill='x', pady=10)

    def gpu_menu_histogram(self):
        self.df['releaseYear'] = self.df['releaseYear'].replace(0, 'Unknown')
        release_year_counts = self.df['releaseYear'].value_counts()
        release_year_counts = release_year_counts[release_year_counts.index != 'Unknown']
        release_year_counts.index = release_year_counts.index.astype(float)

        fig, ax = plt.subplots(figsize=(10, 6))
        release_year_counts.sort_index().plot(
            ax=ax, marker='o', color='orange', linewidth=2)
        ax.set_title('Graphics Cards by Release Year')
        ax.set_xlabel('Release Year')
        ax.set_ylabel('Number of Cards')
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def run(self):
        self.root.mainloop()
