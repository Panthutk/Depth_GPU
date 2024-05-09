import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CompareMode:
    def __init__(self, master, df) -> None:
        self.master = master
        self.df = df
        self.master.title("Compare Mode")
        self.master.geometry("1500x800")
        self.setup_head()
        self.setup_lower_frame()
        self.setup_head_frame()

        self.run()

    def setup_head(self):
        # Create head frame at the top
        self.head_frame = Frame(self.master, height=90, bg='#989898')
        self.head_frame.pack(fill=X)

    def setup_lower_frame(self):
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

        # Create the ComboBox for First manufacturer
        self.first_manufacturer_label = Label(
            self.head_frame, text="Manufacturer:", font=("Arial", 12), bg='#989898')
        self.first_manufacturer_label.pack(side=LEFT, padx=10)

        self.first_manufacturer_combobox = ttk.Combobox(
            self.head_frame, values=[str(val).strip() for val in self.df['manufacturer'].unique()], font=("Arial", 12), state='readonly')
        self.first_manufacturer_combobox.pack(side=LEFT)

        # Create the ComboBox for First GPU names
        self.first_gpu_label = Label(
            self.head_frame, text="GPU:", font=("Arial", 12), bg='#989898')
        self.first_gpu_label.pack(side=LEFT, padx=10)

        self.first_gpu_combobox = ttk.Combobox(
            self.head_frame, font=("Arial", 12), state='readonly')
        self.first_gpu_combobox.pack(side=LEFT)

        # Bind first manufacturer combobox to update the first GPU combobox
        self.first_manufacturer_combobox.bind(
            "<<ComboboxSelected>>", self.update_first_gpu_combobox)

        # Create the ComboBox for Second manufacturer
        self.second_manufacture_label = Label(
            self.head_frame, text="Manufacturer:", font=("Arial", 12), bg='#989898')
        self.second_manufacture_label.pack(side=LEFT, padx=10)

        self.second_manufacture_combobox = ttk.Combobox(
            self.head_frame, values=[str(val).strip() for val in self.df['manufacturer'].unique()], font=("Arial", 12), state='readonly')
        self.second_manufacture_combobox.pack(side=LEFT)

        # Create the ComboBox for Second GPU names
        self.second_gpu_label = Label(
            self.head_frame, text="GPU:", font=("Arial", 12), bg='#989898')
        self.second_gpu_label.pack(side=LEFT, padx=10)

        self.second_gpu_combobox = ttk.Combobox(
            self.head_frame, font=("Arial", 12), state='readonly')
        self.second_gpu_combobox.pack(side=LEFT)

        # Bind second manufacturer combobox to update the second GPU combobox
        self.second_manufacture_combobox.bind(
            "<<ComboboxSelected>>", self.update_second_gpu_combobox)

        self.compare_button = Button(self.head_frame, text="Compare", font=(
            "Arial", 12), bg='#989898', command=self.compare_gpu, width=10, height=2)
        self.compare_button.pack(side=RIGHT, padx=20, pady=18)

    def update_first_gpu_combobox(self, event):
        # Get the selected manufacturer
        first_selected_manufacturer = self.first_manufacturer_combobox.get()

        # Filter DataFrame based on selected manufacturer
        first_gpu_names = self.df[self.df['manufacturer'] ==
                                  first_selected_manufacturer]['productName'].tolist()

        # Update the first GPU combobox
        self.first_gpu_combobox['values'] = sorted(first_gpu_names)

    def update_second_gpu_combobox(self, event):
        # Get the selected manufacturer
        second_selected_manufacturer = self.second_manufacture_combobox.get()

        # Filter DataFrame based on selected manufacturer
        second_gpu_names = self.df[self.df['manufacturer'] ==
                                   second_selected_manufacturer]['productName'].tolist()

        # Update the second GPU combobox
        self.second_gpu_combobox['values'] = sorted(second_gpu_names)

    def compare_gpu(self):
        # Clear the existing text in the left frame
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Clear the existing plot in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Get the selected GPUs and their details
        first_selected_manufacturer = self.first_manufacturer_combobox.get()
        first_selected_gpu = self.first_gpu_combobox.get()

        second_selected_manufacturer = self.second_manufacture_combobox.get()
        second_selected_gpu = self.second_gpu_combobox.get()

        # Define colors for the bar plot
        colors = {'NVIDIA': 'b',
                  'AMD': 'g',
                  'Intel': 'y',
                  '3dfx': 'r',
                  'ATI': 'c',
                  'Matrox': 'm',
                  'Sony': 'k',
                  'XGI': 'orange'
                  }

        # Filter DataFrame based on selected manufacturer and GPU
        first_gpu_details = self.df[(self.df['manufacturer'] == first_selected_manufacturer) & (
            self.df['productName'] == first_selected_gpu)]

        second_gpu_details = self.df[(self.df['manufacturer'] == second_selected_manufacturer) & (
            self.df['productName'] == second_selected_gpu)]

        # Retrieve additional details
        first_additional_details = f"ProductName: {first_selected_gpu}\n" \
            f"Manufacturer: {first_selected_manufacturer}\n" \
            f"MemSize: {first_gpu_details['memSize'].iloc[0]}\n" \
            f"Release year: {first_gpu_details['releaseYear'].iloc[0]}\n" \
            f"IGP: {first_gpu_details['igp'].iloc[0]}\n" \
            f"Bus: {first_gpu_details['bus'].iloc[0]}\n" \
            f"Mem type: {first_gpu_details['memType'].iloc[0]}\n" \
            f"GPU Chip: {first_gpu_details['gpuChip'].iloc[0]}\n" \
            "---------------------------------------\n"
        second_additional_details = f"ProductName: {second_selected_gpu}\n" \
            f"Manufacturer: {second_selected_manufacturer}\n" \
            f"MemSize: {second_gpu_details['memSize'].iloc[0]}\n" \
            f"Release year: {second_gpu_details['releaseYear'].iloc[0]}\n" \
            f"IGP: {second_gpu_details['igp'].iloc[0]}\n" \
            f"Bus: {second_gpu_details['bus'].iloc[0]}\n" \
            f"Mem type: {second_gpu_details['memType'].iloc[0]}\n" \
            f"GPU Chip: {second_gpu_details['gpuChip'].iloc[0]}\n" \
            "---------------------------------------\n"

        # Display additional details in the left frame
        first_additional_label = Label(self.left_frame, text=first_additional_details,
                                       font=("Arial", 12), justify=LEFT, anchor='w')
        first_additional_label.pack(anchor='w')

        second_additional_label = Label(self.left_frame, text=second_additional_details,
                                        font=("Arial", 12), justify=LEFT, anchor='w')
        second_additional_label.pack(anchor='w')

        detail_text = "Summary statistics\n"
        important_specs = ['memBusWidth', 'gpuClock',
                           'memClock']
        important_specs2 = ['unifiedShader', 'tmu', 'rop']
        filtered_important_specs = self.df[self.df[important_specs] != 0]
        filtered_important_specs2 = self.df[self.df[important_specs2] != 0]

        stats = filtered_important_specs[important_specs].agg(
            ['mean', 'std', 'min', 'max'])
        stats2 = filtered_important_specs2[important_specs2].agg(
            ['mean', 'std', 'min', 'max'])

        detail_text += f"{stats.round(2)}\n"
        detail_text += f"{stats2.round(2)}\n"
        # Display GPU details in the left frame
        detail_label = Label(self.left_frame, text=detail_text,
                             font=("Arial", 12), justify=LEFT, anchor='w')
        detail_label.pack(anchor='w')

    def load_menu_page(self):
        # Load the menu page
        self.master.destroy()
        from menu import Menu
        Menu()

    def run(self):
        self.master.mainloop()
