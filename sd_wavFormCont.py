# -*- coding: utf-8 -*-
"""
音の時間波形をリアルタイムで更新表示
Created on Tue Jun 27 11:22:30 2023

@author: Teruki Toya
"""

import sounddevice as sd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# sd.default.device = [1, 4] # Input, Outputデバイス指定

def callback(indata, frames, time, status):
    # indata :[n_samples × n_channels]
    global plotdata
    data = indata[::downsample, 0]
    shift = len(data)
    plotdata = np.roll(plotdata, -shift, axis=0)
    plotdata[-shift:] = data


def update_plot(frame):
    """This is called by matplotlib for each plot update.
    """
    global plotdata
    line.set_ydata(plotdata)
    return line,

downsample = 10
length = int(1000 * 44100 / (1000 * downsample))
plotdata = np.zeros((length))

fig, ax = plt.subplots()
line, = ax.plot(plotdata)
ax.set_ylim([-1.0, 1.0])
ax.set_xlim([0, length])
ax.yaxis.grid(True)
fig.tight_layout()

stream = sd.InputStream(
        channels=1,
        dtype='float32',
        callback=callback
    )
ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
with stream:
    plt.show()
