import numpy as np
import pandas as pd
import scipy.io as sio
import matplotlib.pyplot as plt
import scipy.signal as signal
import os
import tkinter as tk
from tkinter import filedialog

""" 
Moving average, find top 3 averages which correlate with 3 MVC contractions, 
then second classifier: find which of 3 averages has the lowest SD, and use this as average MVC
"""



class moving_average(object):
    print(os.getcwd())

    def __init__(self):
        # Get the data
        # Load data
        # forcedata = sio.loadmat("C:\\Users\\danie\\Documents\\forcedata.mat", squeeze_me=True)

        #Select a file
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        sio.loadmat(file_path)

        # Check shape of data
        self.force = forcedata['Data'].shape
        self.time = forcedata['Time'].shape
        # print(time)
        # print(forcedata['Time'])
        # print(forcedata['Data'])

        # Define variables
        force = forcedata['Data']
        time = forcedata['Time']

        # Plot graph
        self.force = self.force - self.force[0]
        plt.plot(time, self.force)

    def filter(self):
        # Filter with butterworth
        sos = signal.butter(5, 1, 'LP', fs=2048, output='sos')
        filtered = signal.sosfiltfilt(sos, self.force)
        return filtered

    def windowing(self):
        pass


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print('Moving Average Fx')
    sa = moving_average()
