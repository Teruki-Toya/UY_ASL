# -*- coding: utf-8 -*-
"""
音の収録とサウンドデータの保存
Created on Tue Jun 27 11:22:30 2023

@author: Teruki Toya
"""

import sounddevice as sd
import soundfile as sf
import numpy as np

duration = 5  

# デバイス情報関連
# sd.default.device = [1, 4] # Input, Outputデバイス指定
input_device_info = sd.query_devices(device=sd.default.device[1])
fs = int(input_device_info["default_samplerate"])

# 録音
y = sd.rec(int(duration * fs), samplerate=fs, channels=3)
sd.wait() # 録音終了待ち

print(y.shape) #=> (duration * fs, channels)

# 録音信号のNumPy配列をwav形式で保存
sf.write("＜保存したいオーディオデータ（のパス）＞.wav", y, fs)