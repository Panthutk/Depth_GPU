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
        self.setup_lower_frame()

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

        # Create the ComboBox for manufacturer
        self.manufacturer_label = Label(
            self.head_frame, text="Manufacturer:", font=("Arial", 12), bg='#989898')
        self.manufacturer_label.pack(side=LEFT, padx=10)

        self.manufacturer_combobox = ttk.Combobox(
            self.head_frame, values=[str(val).strip() for val in self.df['manufacturer'].unique()], font=("Arial", 12), state='readonly')
        self.manufacturer_combobox.pack(side=LEFT)

        # Create the ComboBox for GPU names
        self.gpu_label = Label(
            self.head_frame, text="GPU:", font=("Arial", 12), bg='#989898')
        self.gpu_label.pack(side=LEFT, padx=10)

        self.gpu_combobox = ttk.Combobox(
            self.head_frame, font=("Arial", 12), state='readonly')
        self.gpu_combobox.pack(side=LEFT)

        # Bind manufacturer selection to event handler
        self.manufacturer_combobox.bind(
            "<<ComboboxSelected>>", self.update_gpu_combobox)

        self.detail_button = Button(self.head_frame, text="Show Detail", font=(
            "Arial", 12), bg='#989898', command=self.show_detail, width=10, height=2)
        self.detail_button.pack(side=RIGHT, padx=20, pady=18)

    def update_gpu_combobox(self, event):
        # Get the selected manufacturer
        selected_manufacturer = self.manufacturer_combobox.get()

        # Filter DataFrame based on selected manufacturer
        gpu_names = self.df[self.df['manufacturer'] ==
                            selected_manufacturer]['productName'].tolist()

        # Update GPU ComboBox with sorted names
        self.gpu_combobox['values'] = sorted(gpu_names)

    def show_detail(self):
        # Clear the existing text in the left frame
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Clear the existing plot in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Get the selected GPU and its details
        selected_manufacturer = self.manufacturer_combobox.get()
        selected_gpu = self.gpu_combobox.get()

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
        gpu_details = self.df[(self.df['manufacturer'] == selected_manufacturer) & (
            self.df['productName'] == selected_gpu)]

        # Retrieve numeric details for the selected GPU
        numeric_details = gpu_details.drop(
            columns=["productName", "manufacturer", "igp", "bus", "memType", "gpuChip"]).iloc[0]

        # Retrieve additional details
        additional_details = f"ProductName: {selected_gpu}\n" \
            f"Manufacturer: {selected_manufacturer}\n" \
            f"MemSize: {gpu_details['memSize'].iloc[0]}\n" \
            f"Release year: {gpu_details['releaseYear'].iloc[0]}\n" \
            f"IGP: {gpu_details['igp'].iloc[0]}\n" \
            f"Bus: {gpu_details['bus'].iloc[0]}\n" \
            f"Mem type: {gpu_details['memType'].iloc[0]}\n" \
            f"GPU Chip: {gpu_details['gpuChip'].iloc[0]}\n" \
            "---------------------------------------\n"

        # Display additional details in the left frame
        additional_label = Label(self.left_frame, text=additional_details,
                                 font=("Arial", 12), justify=LEFT, anchor='w')
        additional_label.pack(anchor='w')

        # Retrieve numeric details for the selected GPU
        numeric_details = gpu_details.drop(
            columns=["productName", "manufacturer", "igp", "bus", "memType", "gpuChip"]).iloc[0]

        # Retrieve average values
        avg_values = self.df.drop(
            columns=["productName", "manufacturer", "igp", "bus", "memType", "gpuChip"]).mean()

        # Prepare the text to display in the left frame
        detail_text = "Short Summary\n"
        for attribute, value in numeric_details.items():
            if attribute == "memBusWidth":
                detail_text += f"{attribute}: {value} is below average.\n"
            else:
                detail_text += f"{attribute}: {value} is above average.\n"
        detail_text += "---------------------------------------\n"

        detail_text += "Summary statistics\n"
        detail_text += "    memBusWidth gpuClock MemClock\n"
        detail_text += f"min:   {self.df['memBusWidth'].min():.2f}          {self.df['gpuClock'].min():.2f}         {self.df['memClock'].min():.2f} \n"
        detail_text += f"max:  {self.df['memBusWidth'].max():.2f}   {self.df['gpuClock'].max():.2f}    {self.df['memClock'].max():.2f} \n"
        detail_text += f"mean: {self.df['memBusWidth'].mean():.2f}    {self.df['gpuClock'].mean():.2f}    {self.df['memClock'].mean():.2f} \n"
        detail_text += f"std:    {self.df['memBusWidth'].std():.2f}     {self.df['gpuClock'].std():.2f}     {self.df['memClock'].std():.2f} \n"
        detail_text += "    unifiedShader   tmu      rop\n"
        detail_text += f"min:   {self.df['unifiedShader'].min():.2f}          {self.df['tmu'].min():.2f}         {self.df['rop'].min():.2f} \n"
        detail_text += f"max:  {self.df['unifiedShader'].max():.2f}   {self.df['tmu'].max():.2f}    {self.df['rop'].max():.2f} \n"
        detail_text += f"mean: {self.df['unifiedShader'].mean():.2f}    {self.df['tmu'].mean():.2f}    {self.df['rop'].mean():.2f} \n"
        detail_text += f"std:    {self.df['unifiedShader'].std():.2f}     {self.df['tmu'].std():.2f}     {self.df['rop'].std():.2f} \n"

        # Display GPU details in the left frame
        detail_label = Label(self.left_frame, text=detail_text,
                             font=("Arial", 12), justify=LEFT, anchor='w')
        detail_label.pack(anchor='w')

        # Plotting in the right frame
        attributes = ["memBusWidth", "gpuClock",
                      "memClock", "unifiedShader", "tmu", "rop"]
        card_values = gpu_details.iloc[0][attributes]

        br1 = np.arange(len(card_values))
        br2 = [x + 0.4 for x in br1]

        fig, ax = plt.subplots()
        ax.bar(br1, card_values, color=colors[selected_manufacturer],
               width=0.4, edgecolor='grey', label=selected_gpu)
        ax.bar(br2, avg_values[attributes], color='#D6ECBD',
               width=0.4, edgecolor='grey', label='Average')

        ax.set_xlabel('Attributes', fontweight='bold', fontsize=15)
        ax.set_ylabel('Values', fontweight='bold', fontsize=15)
        ax.set_xticks([r + 0.2 for r in range(len(card_values))])
        ax.set_xticklabels(attributes)

        ax.set_title("Card Details and Average",
                     fontweight='bold', fontsize=20)
        ax.legend()

        # Embed the plot in the right frame
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def load_menu_page(self):
        # Destroy the current frame and load the menu page
        self.master.destroy()
        from menu import Menu
        Menu()

    def run(self):
        self.master.mainloop()
