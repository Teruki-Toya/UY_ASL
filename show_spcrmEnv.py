# -*- coding: utf-8 -*-
"""
スペクトル包絡の分析
Created on Tue Jun 27 11:30:45 2023

@author: Teruki Toya
"""
# %%
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import analFreq

wavFile = "＜分析したいオーディオデータ（のパス）＞.wav"
x, fs = sf.read(wavFile)
t_dul = (len(x)-1)/fs
t = np.linspace(0, t_dul, len(x))

# 分析時刻（窓の中心）[s]
t_anal = 3.6

# 分析窓長 [sample]（スペクトル微細構造と包絡）
winSize_fine = 2048
winSize_env = 512

# リフタカットオフ
liftSize = 32

# 線形予測次数
lpcOrder = 40

# 分析対象の中心サンプル点
p_anal = int(fs * t_anal)

# 分析区間の切り出し
iF_ini = p_anal - int(winSize_fine / 2)
iF_fin = p_anal + int(winSize_fine / 2)
xw_fine = x[iF_ini : iF_fin]

iE_ini = p_anal - int(winSize_env / 2)
iE_fin = p_anal + int(winSize_env / 2)
xw_env = x[iE_ini : iE_fin]

## FFTスペクトル（微細構造）
freqF, S_fine, p = analFreq.spectrum(xw_fine, fs, winSize_fine)

# ケプストラム法によるスペクトル包絡
freqcE, S_cEnv = analFreq.spcrmEnv_cepst(xw_env, fs, liftSize)

# 線形予測（LP）によるスペクトル包絡
freqlE, S_lEnv = analFreq.spcrmEnv_lpc(xw_env, fs, lpcOrder)

# プロット
l0, l1, l2 = "FFT spectrum", "Cepstrum envelope", "LPC envelope"
plt.plot(freqF, S_fine, ls = ":", linewidth = 1.0, label = l0)
plt.plot(freqcE, S_cEnv, ls = "-", linewidth = 2.5, label = l1)
plt.plot(freqlE, S_lEnv, ls = "-", linewidth = 2.5, label = l2)
plt.xlabel("Frequency [Hz]", fontsize = 13)
plt.ylabel("Amplitude [dB]", fontsize = 13)
plt.xlim([0,freqF[-1]])
plt.legend(fontsize = 13)
plt.tick_params(labelsize=10)

plt.show()

# %%
