# -*- coding: utf-8 -*-

"""
長時間平均スペクトル（Long-Term Average Spectrum: LTAS）の分析
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

# 分析窓長 [samples]
winSize = 256
  
# フレームシフト長 [samples]
shiftSize = int(winSize / 2)

# FFT長 [sample]
fftSize = winSize

Xf_frm = analFreq.specByFrm(x, fs, winSize, shiftSize, fftSize)

Xf_mean = np.mean(Xf_frm, axis=0)

# 分析対象の周波数列
idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
freq = idx * fs / fftSize

# 振幅スペクトル
S_amp = abs(Xf_mean) / fftSize
S_amp = 2 * S_amp[0 : len(freq)]  # 片側スペクトル
S_amp = 20 * np.log10(S_amp / np.amax(S_amp)) # 相対レベル表現

# プロット
plt.plot(freq, S_amp)
plt.title("Amplitude Spectrum")
plt.xlabel("Frequency [Hz]", fontsize = 13)
plt.ylabel("Magnitude [dB]", fontsize = 13)
plt.xlim([0,freq[-1]])
plt.tick_params(labelsize=10)

plt.show()
