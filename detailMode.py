import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DetailMode:
    def __init__(self, master, df) -> None:
        self.master = master
        self.df = df
        self.master.title("Detail Mode")
        self.master.geometry("1300x800")
        self.setup_frames()

    def setup_frames(self):
        # Create head frame at the top
        self.head_frame = Frame(self.master, height=90, bg='#989898')
        self.head_frame.pack(fill=X)

        # Create a frame container for the lower part
        self.lower_frame = Frame(self.master)
        self.lower_frame.pack(fill=BOTH, expand=True)

    def show_gpu_info_and_graph(self):
        # Create left frame below head frame
        self.left_frame = Frame(
            self.lower_frame, width=410, height=710, bg='#F3F2F2')
        self.left_frame.pack(side=LEFT, fill=Y)

        # Create right frame which takes the rest of the space
        self.right_frame = Frame(self.lower_frame, bg='white')
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True)
