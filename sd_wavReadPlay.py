# -*- coding: utf-8 -*-

"""
wavオーディオデータの読み込みと再生
Created on Tue Jun 27 11:30:45 2023

@author: Teruki Toya
"""

import numpy as np
import soundfile as sf
import sounddevice as sd

# sd.default.device = [1, 8] # Input, Outputデバイスを指定

# WAVファイルの相対パス
wavFilePath = "＜分析したいオーディオデータ（のパス）＞.wav"

# WAV ファイルを読み込み変数に格納
x, fs = sf.read(wavFilePath)
sd.play(x, fs)
