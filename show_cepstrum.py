# -*- coding: utf-8 -*-

"""
ケプストラムの図示
Created on Tue Jun 27 11:30:45 2023

@author: Teruki Toya
"""

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import analFreq

wavFile = "＜分析したいオーディオデータ（のパス）＞.wav"
x, fs = sf.read(wavFile)
t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))

# 分析時刻（窓の中心）[s]
t_anal = 0.5

# 分析窓長
winSize = 1024

p_anal = round(fs * t_anal)

i_ini = round(p_anal - int(winSize / 2))
i_fin = round(p_anal + int(winSize / 2))
xw = x[i_ini : i_fin]

xc = analFreq.cepstrum(xw, winSize)

quef = np.linspace(0, int(1000*(winSize/2)/fs), int(winSize/2+1))
Cep = xc[0 : len(quef)].real

plt.plot(quef, Cep)
plt.xlabel("Quefrency [ms]")
plt.ylabel("Cepstrum value")
plt.xlim([0,quef[-1]])
plt.ylim([-0.5, 0.5])

plt.show()
