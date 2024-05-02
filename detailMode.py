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

        self.run()

    def run(self):
        self.master.mainloop()
