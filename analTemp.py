# -*- coding: utf-8 -*-

# < 信号に対する時間的操作の関数群 >

import numpy as np

## 自己相関関数 ---------------------------------------------
def corrAuto(x, order = 0):
  """
  < 入力 >
    x:  分析対象の時間波形（系列データ）
    [order: 次数 --> デフォルトは x の信号長と同じ]
  < 出力 >
    r:  自己相関関数（系列データ）
  """
  if order <= 0:
    r = np.zeros(len(x))
  else:
    r = np.zeros(order + 1)

  for m in range(len(r)):
    for n in range(len(x) - m):
      r[m] = r[m] + x[n] * x[n + m]
  
  return r

## 2つの信号の時間的同期 ---------------------------------------------
def sigsTimeSyncronize(sig1, sig0):
  """
  < 入力 >
    sig1:  時間同期したい対象の信号（系列データ）
    sig0:  時間同期する基準の信号（系列データ）
  < 出力 >
    sig1r:  基準信号に時間同期された対象信号（系列データ）
  """  
  if len(sig0) > len(sig1):
    sig1 = sig1, np.zeros(len(sig0)-len(sig1))
  elif len(sig0) < len(sig1):
    sig1 = sig1[0:len(sig0)]
  
  c = np.correlate(sig1, sig0, "full")
  d = c.argmax() - (len(sig0) - 1)
  
  if d > 0:
    sig1r = np.concatenate([sig1[d:], sig1[0:d]])
  elif d < 0:
    sig1r = np.concatenate([sig1[len(sig1)+d:], sig1[0:len(sig1)+d]])

  return sig1r

## シフトしながら短時間フレームに分割 -----------------------------
def shiftFrmDiv(x, fs, winSize, shiftSize = -9999):
  """
  < 入力 >
    x:  分析対象の時間波形（系列データ）
    fs: サンプリング周波数 [Hz]
    winSize: 窓長（フレームサンプル数）
    [shiftSize: フレームシフト長 --> デフォルトは窓長の半分]
  < 出力 >
    x_frm:  フレームごとに分割されたデータ [フレーム数 × 窓長]
  """
  
  # 窓のシフト長
  if shiftSize < 0:
    shiftSize = int(winSize / 2)
  
  # 総フレーム数
  N_frame = int(np.floor((len(x) - (winSize - shiftSize)) / shiftSize))
  
  # フレームごとに分割した波形行列 [フレーム数 × 窓長]
  x_frm = np.zeros((N_frame, winSize))
  for frame in range(N_frame):
    offset = shiftSize * frame  # フレームをシフトしながら
    s = x[offset : offset + winSize]
    x_frm[frame, :] = s
  
  return x_frm