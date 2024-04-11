from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Depth Gpu Comparison")
        self.root.geometry("800x600")

        self.run()

    def run(self):
        self.root.mainloop()
