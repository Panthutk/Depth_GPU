import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from compareMode import CompareMode
from detailMode import DetailMode


class Menu:
    def __init__(self) -> None:
        # Create the menu window
        self.root = Tk()
        self.root.title("Depth GPU Comparison")
        self.root.geometry("1200x600")
        self.read_csv()

        self.setup_frames()
        self.menu_page()
        self.gpu_menu_menu_graph()

        self.run()

    def read_csv(self):
        # Read the csv file
        self.df = pd.read_csv('Clean_gpu_specs_v6.csv')

    def setup_frames(self):
        # Create the left and right frames
        self.left_frame = Frame(self.root, width=200, bg='gray')
        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.right_frame = Frame(self.root, width=1000, bg='white')
        self.right_frame.grid(row=0, column=1, sticky="nswe")

        # Configure column and row for frames
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=5)
        self.root.grid_rowconfigure(0, weight=1)

    def menu_page(self):
        # Create the menu page
        Label(self.left_frame, text="DGC", font=(
            "Arial", 24), bg='gray').pack(pady=20)
        Label(self.left_frame, text=f'Last updated: {int(max(self.df["releaseYear"]))}', font=(
            "Arial", 10), bg='gray').pack(pady=10)
        Button(self.left_frame, text="Compare Mode",
               command=self.load_compare_mode).pack(fill='x', pady=10)
        Button(self.left_frame, text="Detail Mode",
               command=self.load_detail_mode).pack(fill='x', pady=10)

    def show_gpu_menu_graph(self):
        pass

    def corelation_coefficient(self):
        self.df['gpuClock'] = self.df['gpuClock'].replace(0, 'Unknown')
        self.df['memClock'] = self.df['memClock'].replace(0, 'Unknown')

        # Convert 'gpuClock' and 'memClock' columns to numeric type, ignoring errors
        self.df['gpuClock'] = pd.to_numeric(
            self.df['gpuClock'], errors='coerce')
        self.df['memClock'] = pd.to_numeric(
            self.df['memClock'], errors='coerce')

        # Filter out 'Unknown' values
        filtered_df = self.df.dropna(subset=['gpuClock', 'memClock'])

        # Calculate correlation coefficient
        correlation_coefficient = filtered_df['gpuClock'].corr(
            filtered_df['memClock'])

        # Plotting scatter plot
        plt.figure(figsize=(8, 6))
        plt.scatter(filtered_df['gpuClock'],
                    filtered_df['memClock'], color='blue', alpha=0.5)
        plt.title('Scatter Plot: GPU Clock vs Memory Clock')
        plt.xlabel('GPU Clock')
        plt.ylabel('Memory Clock')
        plt.grid(True)
        plt.show()

        print("Correlation Coefficient between GPU Clock and Memory Clock:",
              correlation_coefficient)

    def histogram_for_release_year(self):
        release_year_counts = self.df['releaseYear'].replace(
            0, 'Unknown').value_counts()

        # Exclude 'Unknown' category
        release_year_counts = release_year_counts[release_year_counts.index != 'Unknown']

        # Plotting histogram for Release Year
        plt.figure(figsize=(8, 6))
        plt.hist(release_year_counts.index.astype(int), bins=10,
                 weights=release_year_counts.values, color='skyblue', edgecolor='black')
        plt.title('Distribution of Release Year')
        plt.xlabel('Release Year')
        plt.ylabel('Frequency')
        plt.grid(axis='y', alpha=0.5)
        plt.show()

    def load_compare_mode(self):
        # Clear the frames
        for widget in self.left_frame.winfo_children():
            widget.destroy()
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Load the compare mode
        compare_mode = CompareMode(self.df)
        compare_mode.run()

    def load_detail_mode(self):
        # Clear the frames
        for widget in self.left_frame.winfo_children():
            widget.destroy()
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Load the detail mode
        detail_mode = DetailMode(self.df)
        detail_mode.run()

    def run(self):
        # Run the main loop
        self.root.mainloop()
