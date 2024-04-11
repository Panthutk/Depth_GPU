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
        self.root.geometry("800x600")

        self.run()

    def run(self):
        self.root.mainloop()