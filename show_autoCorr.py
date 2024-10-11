# -*- coding: utf-8 -*-
"""
自己相関関数の図示
Created on Tue Jun 27 11:30:45 2023

@author: Teruki Toya
"""

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import analTemp

wavFile = "＜分析したいオーディオデータ（のパス）＞.wav"
x, fs = sf.read(wavFile)
t = np.linspace(0, len(x) - 1, len(x)) / fs

# 分析時刻（窓の中心）[s]
t_anal = 0.5

# 分析窓長
winSize = 1024

# 分析対象の中心サンプル点
p_anal = round(fs * t_anal)

# 分析区間の切り出し
i_ini = round(p_anal - int(winSize / 2))
i_fin = round(p_anal + int(winSize / 2))
xw = x[i_ini : i_fin]

# 分析区間の総パワー
den = np.sum(xw**2)

# 自己相関
r = analTemp.corrAuto(xw)
r = r / den

t = np.linspace(0, 1000*(winSize - 1)/fs, winSize)
Corr = r[0 : len(t)]

# プロット
plt.plot(t, Corr)
plt.xlabel("Time [ms]")
plt.ylabel("Autocorrelation value")
plt.xlim([0,t[-1]])
plt.ylim([-1, 1])

plt.show()
