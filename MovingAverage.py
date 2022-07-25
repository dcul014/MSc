import numpy as np
import pandas as pd
from scipy.io import loadmat
import matplotlib.pyplot as plt
import scipy.signal as signal
import os
import tkinter as tk
from tkinter import filedialog
import heapq

""" 
Moving average, find top 3 averages which correlate with 3 MVC contractions, 
then second classifier: find which of 3 averages has the lowest SD, and use this as average MVC
"""

class Moving_Average(object):
    print(os.getcwd())

    def __init__(self):

        try:
            '''numpy array from a matlab .mat file'''
            data_set = loadmat("forcedata.mat", squeeze_me=True)
            # Define variables
            self.force = data_set['Data']
            self.time = data_set['Time']
            self.sfreq = data_set['SamplingFrequency']
        except:
            # Select a file
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            data_set = loadmat(file_path, squeeze_me=True)
            # Define variables
            self.force = data_set['Data']
            self.time = data_set['Time']
            self.sfreq = data_set['SamplingFrequency']

        plt.plot(self.time, self.force)
        fforce = self.filter()
        plt.figure(1)
        plt.plot(self.time, fforce)
        self.windowing(fforce)
        plt.show()

    def filter(self):
        # Filter with butterworth
        b, a = signal.butter(2, 4/(0.5*2048))
        filtered = signal.filtfilt(b, a, self.force)
        return filtered

    def windowing(self, data):
        window_size = self.sfreq / 2
        stride = window_size / 2
        print('here')
        window_avg = [np.mean(data[i:i + int(window_size)]) for i in range(0, len(data), int(stride))
                      if i + window_size <= len(data)]
        window_std = [np.std(data[i:i + int(window_size)]) for i in range(0, len(data), int(stride))
                      if i + window_size <= len(data)]

        f_largest = heapq.nlargest(3, range(len(window_avg)), window_avg.__getitem__)
        min_val = min(window_std[i] for i in f_largest)
        min_index = window_std.index(min_val)

        print('Index of max force = ', min_index*512, ' - ', (min_index*512)+ 512)
        print('Max Value force = ', window_avg[min_index])


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print('Moving Average Fx')
    sa = Moving_Average()