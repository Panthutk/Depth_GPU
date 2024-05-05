import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CompareMode:
    def __init__(self, master, df) -> None:
        self.master = master
        self.df = df
        self.master.title("Compare Mode")
        self.master.geometry("1300x800")
