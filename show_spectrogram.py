# -*- coding: utf-8 -*-
"""
スペクトログラムの図示
Created on Tue Jun 27 11:30:45 2023

@author: Teruki Toya
"""
# %%
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import analFreq

# 音声データの取得
filepath = "vowelTest.wav"
x, fs = sf.read(filepath)
x = x[:, 0]

t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))


# 分析窓長
winSize = 256

t, freq, Sa = analFreq.spgram(x, fs, winSize)

plt.imshow(Sa, cmap="jet", extent=[0, t[-1], 0, freq[-1]], aspect="auto", vmin=-100, vmax=10)
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
#plt.xlim([1, 2])
plt.ylim([0, 22050])
plt.colorbar()
plt.show()

# %%
