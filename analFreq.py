# -*- coding: utf-8 -*-

# < 基本的な周波数解析の関数群 >

import numpy as np
import numpy.matlib as nmat
import scipy.fftpack as spfft
import wdFunc
import lpcas

## 窓かけありの短時間スペクトル ---------------------------------------------
def spectrum(x, fs, fftSize):
  """
  < 入力 >
    x:  分析対象の時間波形（系列データ）
    fs: サンプリング周波数 [Hz]
    fftSize:  FFT長（サンプル数）
  < 出力 >
    freq:  分析対象の周波数列（系列データ）[Hz]
    S_amp: 振幅スペクトル（系列データ）[dB]
    S_phase:  位相スペクトル（系列データ）[deg]
  """

  # 分析窓をかける
  w = wdFunc.winHann(len(x))
  xw = x * w
  
  # 高速フーリエ変換（FFT）
  X = spfft.fft(xw, fftSize)
  
  # 分析対象の周波数列
  idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
  freq = idx * fs / fftSize
  
  # 振幅スペクトル
  S_amp = abs(X) / fftSize
  S_amp = 2 * S_amp[0 : len(freq)]  # 片側スペクトル
  S_amp = 20 * np.log10(S_amp)  # レベル表現 [dB]
  
  # 位相スペクトル
  S_phase = np.unwrap(np.angle(X))
  S_phase = S_phase[0 : len(freq)]  # 片側スペクトル
  
  return freq, S_amp, S_phase

## 短時間フレームシフトによるスペクトル行列の生成 -----------------------------
def specByFrm(x, fs, winSize, shiftSize = -9999, fftSize = -9999):
  """
  < 入力 >
    x:  分析対象の時間波形（系列データ）
    fs: サンプリング周波数 [Hz]
    winSize: 窓長（フレームサンプル数）
    [shiftSize: フレームシフト長 --> デフォルトは窓長の半分]
    [fftSize: FFT長 --> デフォルトは窓長と同じ]
  < 出力 >
    Xf_frm:  複素スペクトルの行列データ [フレーム数 × FFT長]
  """
  
  # 窓のシフト長
  if shiftSize < 0:
    shiftSize = int(winSize / 2)
  
  # FFT長
  if fftSize < 0:
    fftSize = winSize
  
  # 総フレーム数
  N_frame = int(np.floor((len(x) - (winSize - shiftSize)) / shiftSize))
  
  # フレームごとに分割した波形行列 [フレーム数 × 窓長]
  x_frm = np.zeros((N_frame, winSize))
  for frame in range(N_frame):
    offset = shiftSize * frame  # フレームをシフトしながら
    s = x[offset : offset + winSize]
    x_frm[frame, :] = s
  
  w = nmat.repmat(wdFunc.winHann(winSize), N_frame, 1)
  x_frmw = x_frm * w	# 分析窓をかける

  Xf_frm = spfft.fft(x_frmw, fftSize, 1)  # 高速フーリエ変換（FFT）

  return Xf_frm

## スペクトログラム ------------------------------------------------
def spgram(x, fs, winSize, shiftSize = -9999, fftSize = -9999):
  """
  < 入力 >
    x:  分析対象の時間波形（系列データ）
    fs: サンプリング周波数 [Hz]
    winSize: 窓長（フレームサンプル数）
    [shiftSize: フレームシフト長 --> デフォルトは窓長の半分]
    [fftSize: FFT長 --> デフォルトは窓長と同じ]
  < 出力 >
    t:  時間サンプル列（系列データ）[s]
    freq: 周波数サンプル列（系列データ）[Hz]
    SaT:  スペクトログラム
  """ 

  # 窓のシフト長
  if shiftSize < 0:
    shiftSize = int(winSize / 2)
  
  # FFT長
  if fftSize < 0:
    fftSize = winSize
  
  # 周波数列
  idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
  freq = idx * fs / fftSize
  
  # フレームごとに分割してスペクトル行列を生成
  Xf_frm = specByFrm(x, fs, winSize, shiftSize, fftSize)
  N_frame = len(Xf_frm)
  
  # 振幅スペクトル
  Sa_frm = abs(Xf_frm) / fftSize
  Sa_frm = 2 * Sa_frm[:, 0 : len(freq)]  # 片側スペクトル
  Sa_frm = 20 * np.log10(Sa_frm)  # レベル表現 [dB]

  Sa_frm = np.fliplr(Sa_frm)  #  周波数方向を反転
  
  SaT = Sa_frm.T 		# 転置（時間を横方向、周波数を縦方向に）
  ids = np.linspace(0, N_frame - 1, N_frame)
  t = ids * shiftSize / fs  # 時間サンプル列
  
  return t, freq, SaT


## ケプストラム  ------------------------------------------------
def cepstrum(x, fftSize):
  """
  < 入力 >
    x:  分析対象の時間波形（系列データ）
    fftSize: FFT長（サンプル数）
  < 出力 >
    xc:  ケプストラム係数（系列データ）
  """   
  # 分析窓をかける
  w = wdFunc.winHann(len(x))
  xw = x * w
  
  # 高速フーリエ変換（FFT）
  X = spfft.fft(xw, fftSize)
  
  # 対数スペクトル
  A = np.log10(abs(X))
  
  # 逆フーリエ変換
  xc = spfft.ifft(A, fftSize)

  return xc


## ケプストラム法によるスペクトル包絡の分析 -----------------------
def spcrmEnv_cepst(x, fs, liftSize, fftSize = -9999):
  """
  < 入力 >
    x:  分析対象の時間波形（系列データ）
    fs: サンプリング周波数 [Hz]
    liftSize: リフタサイズ（サンプル数）
    [fftSize: FFT長 --> デフォルトは x の信号長と同じ]
  < 出力 >
    freq: 周波数サンプル列（系列データ）[Hz]
    XC_amp:  スペクトル包絡（系列データ）[dB]
  """ 
  # FFT長
  if fftSize < 0:
    fftSize = len(x)
  
  # ケプストラム
  xc = cepstrum(x, fftSize)
  
  # 低ケフレンシ成分以外を 0 埋め
  xc[liftSize : len(xc) - liftSize] = np.zeros(len(xc) - 2 * liftSize)

  # 低ケフレンシ成分のフーリエ変換
  XC = spfft.fft(xc, fftSize)
  
  # 分析対象の周波数列
  idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
  freq = idx * fs / fftSize
  
  # dB 表現（すでに対数スペクトルになっているので、20 のみ乗算）
  XC_amp = 20 * XC.real
  XC_amp = XC_amp[0 : len(freq)]
  
  return freq, XC_amp


## 線形予測（LP）によるスペクトル包絡の分析 -----------------------
def spcrmEnv_lpc(x, fs, lpcOrder, fftSize = -9999, preEnp = 1, coeff = 0.98):
  """
  < 入力 >
    x:  分析対象の時間波形（系列データ）
    fs: サンプリング周波数 [Hz]
    lpcOrder: 線形予測次数
    [fftSize: FFT長 --> デフォルトは x の信号長と同じ]
    [preEmp: プリエンファシスの有無 --> デフォルトは 1（有）]
    [coeff: プリエンファシス係数 --> デフォルトは 0.98]
  < 出力 >
    freq: 周波数サンプル列（系列データ）[Hz]
    VTfilt:  声道順フィルタ（系列データ）[dB]
  """ 
  # FFT長
  if fftSize < 0:
    fftSize = len(x)
  
  # プリエンファシス
  if preEnp == 0:
    x0 = x
  else:
    xtmp = np.append(0, x[0 : len(x) - 1])
    x0 = x - coeff * xtmp
    x0[0] = 0
  
  # 分析窓をかける
  w = wdFunc.winHann(len(x))
  x0w = x0 * w
  
  # 線形予測分析
  x_lpc, parcor = lpcas.LDcalc(x0w, lpcOrder)
  
  # フーリエ変換
  X = spfft.fft(x_lpc, fftSize)
  
  # 分析対象の周波数列
  idx = np.linspace(0, int(fftSize/2), int(fftSize/2+1))
  freq = idx * fs / fftSize
  
  # 声道順フィルタ（分子／分母が逆転（dB 表現では符号反転））
  VTfilt = -20 * np.log10(abs(X))
  VTfilt = VTfilt[0 : len(freq)]
  
  return freq, VTfilt
