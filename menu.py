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
        self.show_gpu_menu_graph()

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
        Button(self.left_frame, text="Quit",
               command=self.root.quit).pack(fill='x', pady=10)

    def show_gpu_menu_graph(self):
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        self.corelation_coefficient(axs[0, 0])
        self.histogram_for_release_year(axs[0, 1])
        self.mem_bus_width_distribution(axs[1, 0])
        self.unified_shader_pie_chart(axs[1, 1])

        fig.tight_layout()  # Adjust layout of the entire figure

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def corelation_coefficient(self, ax):
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
        ax.scatter(filtered_df['gpuClock'],
                   filtered_df['memClock'], color='blue', alpha=0.5)
        ax.set_title('Scatter Plot: GPU Clock vs Memory Clock')
        ax.set_xlabel('GPU Clock')
        ax.set_ylabel('Memory Clock')
        ax.grid(True)

        print("Correlation Coefficient between GPU Clock and Memory Clock:",
              correlation_coefficient)

    def histogram_for_release_year(self, ax):
        release_year_counts = self.df['releaseYear'].replace(
            0, 'Unknown').value_counts()

        # Exclude 'Unknown' category
        release_year_counts = release_year_counts[release_year_counts.index != 'Unknown']

        # Plotting histogram for Release Year
        ax.hist(release_year_counts.index.astype(int), bins=10,
                weights=release_year_counts.values, color='skyblue', edgecolor='black')
        ax.set_title('Distribution of Release Year')
        ax.set_xlabel('Release Year')
        ax.set_ylabel('Frequency')
        ax.grid(axis='y', alpha=0.5)

    def mem_bus_width_distribution(self, ax):
        mem_bus_width_counts_filtered = self.df[self.df['memBusWidth']
                                                != 0]['memBusWidth'].value_counts().sort_index()

        # Plotting the horizontal bar plot
        mem_bus_width_counts_filtered.plot(kind='barh', color='skyblue', ax=ax)
        ax.set_title('Memory Bus Width Distribution')
        ax.set_xlabel('Count')
        ax.set_ylabel('Memory Bus Width')
        ax.grid(axis='x', alpha=0.5)

    def unified_shader_pie_chart(self, ax):
        # Filter out zero counts
        non_zero_counts = self.df[self.df['unifiedShader']
                                  != 0]['unifiedShader'].value_counts()

        # Select the top five non-zero counts
        top_five_non_zero_counts = non_zero_counts.head()

        # Plot the pie chart
        ax.pie(top_five_non_zero_counts, labels=top_five_non_zero_counts.index,
               autopct='%1.1f%%', colors=plt.cm.Set2.colors)
        ax.set_title('Unified Shader Counts')

    def load_compare_mode(self):
        # Clear the frames
        for widget in self.root.winfo_children():
            widget.destroy()

        # Load the compare mode
        compare_mode = CompareMode(self.root, self.df)
        compare_mode.run()

    def load_detail_mode(self):
        # Clear the frames
        for widget in self.root.winfo_children():
            widget.destroy()

        # Load the detail mode
        detail_mode = DetailMode(self.root, self.df)
        detail_mode.run()

    def run(self):
        # Run the main loop
        self.root.mainloop()


# Instantiate the Menu class to run the application
if __name__ == "__main__":
    menu = Menu()
