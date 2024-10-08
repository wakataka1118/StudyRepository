# -*- coding: utf-8 -*-
"""タブーのみIDE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12Hmd0p2hNRkZhqJmUJ24_InmlQi4-hfD
"""

import math
import colorsys

#HSV形式からRGB形式に変換する関数
#R=0 ~ 255, G=0 ~ 255, B=0 ~ 255,
def hsv_to_rgb(h,s,v):
#    h = 0 ~ 360
#    s = 0 ~ 100
#    v = 0 ~ 100
    h = h * 360
    s = s * 100
    v = v *100

    if h == 360:
      h = 0

    h_ = (h / 60) % 1
    s_ = s / 100
    v_ = v / 100

    A = v_ * 255
    B = v_ * (1 - s_) * 255
    C = v_ * (1 - s_ * h_) * 255
    D = v_ * (1 - s_ * (1 - h_)) * 255

    if s == 0:
      return [A, A, A]
    elif 0<=h<60:
      return [A, D, B]
    elif 60<=h<120:
      return [C, A, B]
    elif 120<=h<180:
      return [B, A, D]
    elif 180<=h<240:
      return [B, C, A]
    elif 240<=h<300:
      return [D, B, A]
    elif 300<=h<360:
      return [A, B, C]

def RGB_to_XYZ(r, g, b):
  # RGB(0~255)=>RGB(0~1.0)
  fix_r = r / 255
  fix_g = g / 255
  fix_b = b / 255

  X = (0.4124 * fix_r) + (0.3576 * fix_g) + (0.1805 * fix_b)
  Y = (0.2126 * fix_r) + (0.7152 * fix_g) + (0.0722 * fix_b)
  Z = (0.0193 * fix_r) + (0.1192 * fix_g) + (0.9505 * fix_b)

  return [X, Y, Z]

def XYZ_to_Lab(x, y, z):
  x_p = x * (100.0 / 95.047)
  y_p = y
  z_p = z * (100.0 / 108.883)

  if x_p > 0.008856:
    x_p = math.pow(x_p, 1/3)
  else:
    x_p = (7.787*x_p) + 16/116

  if y_p > 0.008856:
    y_p = math.pow(y_p, 1/3)
  else:
    y_p = (7.787*y_p) + 16/116

  if z_p > 0.008856:
    z_p = math.pow(z_p, 1/3)
  else:
    z_p = (7.787*z_p) + 16/116

  L = (116 * y_p) - 16
  a = 500 * (x_p - y_p)
  b = 200 * (y_p - z_p)

  return [L, a, b]

def ciede2000(L1, a1, b1, L2, a2, b2):
  # CIEDE2000距離を導出する関数
  kL= 1.0
  kC= 1.0
  kH= 1.0
  # Hは色相, Sは彩度，　Vは明度
  delta_Lp = L2 - L1 # デルタVの導出
  L_ = (L1 + L2) / 2 # 明度の平均
  C1 = math.sqrt(math.pow(a1, 2) + math.pow(b1, 2))
  C2 = math.sqrt(math.pow(a2, 2) + math.pow(b2, 2))
  C_ = (C1 + C2) / 2 # 彩度の平均
  ap1 = a1 + (a1 / 2) * (1 - math.sqrt(math.pow(C_, 7) /(math.pow(C_, 7) + math.pow(25, 7))))
  ap2 = a2 + (a2 / 2) * (1 - math.sqrt(math.pow(C_, 7) /(math.pow(C_, 7) + math.pow(25, 7))))
  Cp1 = math.sqrt(math.pow(ap1, 2) + math.pow(b1, 2))
  Cp2 = math.sqrt(math.pow(ap2, 2) + math.pow(b2, 2))
  Cp_ = (Cp1 + Cp2) / 2
  delta_Cp = Cp2 - Cp1 # デルタCの導出

  hp1 = 0.0
  if ap1 == 0 and b1 == 0:
    hp1 = 0
  else:
    hp1 = (180 / math.pi) * (math.atan2(b1, ap1))
    if hp1 < 0.0:
      hp1 = hp1 + 360

  hp2 = 0.0
  if ap2 == 0 and b2 == 0:
    hp2 = 0
  else:
    hp2 = (180 / math.pi) * (math.atan2(b2, ap2))
    if hp2 < 0.0:
      hp2 = hp2 + 360

  delta_hp = 0.0
  # デルタhを条件分岐を利用して，導出する
  if C1 == 0.0 or C2 == 0.0:
    delta_hp = 0.0
  elif abs(hp1 - hp2) <= 180:
    delta_hp = hp2 - hp1
  elif hp2 <= hp1:
    delta_hp = hp2 - hp1 + 360
  else: #abs(H1 - H2) > 0.5 and H2 > H1の時
    delta_hp = hp2 - hp1 - 360

  # デルタHを条件分岐を利用して，導出する
  delta_Hp = 2 * math.sqrt(Cp1 * Cp2) * math.sin((delta_hp * (math.pi / 180)) / 2)

  # Hの平均を条件分岐を利用して，導出する
  if C1 == 0 or C2 == 0:
    Hp_ = hp1 + hp2
  elif abs(hp1 - hp2) <= 180:
    Hp_ = (hp1 + hp2) / 2
  elif abs(hp1 - hp2) > 180 and hp1 + hp2 < 360:
    Hp_ = (hp1 + hp2 + 360) / 2
  else: #abs(hp1 - hp2) > 180 and hp1 + hp2 >= 360の時
    Hp_ = (hp1 + hp2 - 360) / 2

  T = 1 - 0.17 * math.cos((Hp_ - 30) * (math.pi / 180)) \
      + 0.24 * math.cos((2 * Hp_) * (math.pi / 180)) \
      + 0.32 * math.cos((3 * Hp_ + 6) * (math.pi / 180)) \
      - 0.20 * math.cos((4 * Hp_  - 63) * (math.pi / 180))

  SL = 1 + (0.015 * math.pow(L_ - 50, 2)) / math.sqrt(20 + math.pow(L_ - 50, 2))
  SC = 1 + 0.045 * Cp_
  SH = 1 + 0.015 * Cp_ * T

  RT1 = math.pow(Cp_, 7) / (math.pow(Cp_, 7) + math.pow(25, 7))
  RT2 = math.sin((60 * math.exp(-1 * math.pow((Hp_ - 275) / 25, 2))) * (math.pi / 180))
  RT = -2 * math.sqrt(RT1 * RT2)

  dis1 = math.pow(delta_Lp / (kL * SL), 2)
  dis2 = math.pow(delta_Cp / (kC * SC), 2)
  dis3 = math.pow(delta_Hp / (kH * SH), 2)
  dis4 = RT * (delta_Cp / (kC * SC)) * (delta_Hp / (kH * SH))

  dis = math.sqrt(dis1 + dis2 + dis3 + dis4)

  return dis

def get_dis_ciede2000(H, S, V, ans_H, ans_S, ans_V):
  # 目標個体とのCIEDE2000距離を返す関数
  rgb = hsv_to_rgb(H, S, V) #HSV値＝＞RGB値に変更
  ans_rgb = hsv_to_rgb(ans_H, ans_S, ans_V)  #目標個体のHSV値＝＞RGB値に変更
  # print("rgb=", rgb)
  xyz = RGB_to_XYZ(rgb[0], rgb[1], rgb[2])  #RGB値＝＞xyz値に変更
  ans_xyz = RGB_to_XYZ(ans_rgb[0], ans_rgb[1], ans_rgb[2]) #目標個体のRGB値＝＞xyz値に変更
  lab = XYZ_to_Lab(xyz[0], xyz[1], xyz[2]) #xyz値＝＞Lab値に変更
  ans_lab = XYZ_to_Lab(ans_xyz[0], ans_xyz[1], ans_xyz[2]) #目標個体のxyz値＝＞Lab値に変更
  return ciede2000(lab[0], lab[1], lab[2], ans_lab[0], ans_lab[1], ans_lab[2])

# 正規化させる関数
def Normalization_Hue(H):
  # 色相の正規化
  if H < 0:
    while H < 0:
      H = 1.0 + H
  elif H > 1.0:
    while H > 1.0:
      H = H - 1.0
  return H

def Normalization_Saturaton_or_Lightness(SV):
  # 彩度，明度の正規化
  while (SV < 0.0) or (SV > 1.0):
    if SV < 0.0:
      SV = SV * (-1)
    elif SV > 1.0:
      SV = 1.0 - (SV - 1.0)
  return SV

import math
import random
Hue_Yellow = 0.55

# 配色技法の関数
def NaturalColor(base_Color):
  # ナチュラル配色で初期個体作成
  next_Color = [0.0, 0.0, 0.0]
  # 彩度の決定
  if (0<= base_Color[1] < 0.05) or (0<= base_Color[2] < 0.15):
    # 無彩色の場合
    rnd = random.uniform(0.0, 1.0)
    next_Color[1] = rnd
  else:
    next_Color[1] = base_Color[1]

  diff_Base = math.fabs(base_Color[0] - Hue_Yellow)
  n = 0
  if 0.7 < base_Color[2] < 1.0:
    if 0.33 <= base_Color[0] < 0.83:
      n = 2
    else:
      n = -2
  elif 0.0 < base_Color[2] < 0.3:
    if 0.33 <= base_Color[0] < 0.83:
      n = 2
    else:
      n = -2
  else:
    rnd = random.randint(0, 1)
    if rnd == 0:
      n = -2
    elif rnd == 1:
      n = 2

  H_Assort = base_Color[0] + n*0.04
  diff_Assort = math.fabs(H_Assort - Hue_Yellow)

  next_Color[0] = H_Assort
  if diff_Base < diff_Assort:
    next_Color[2] = base_Color[2] - 0.35
  else:
    next_Color[2] = base_Color[2] + 0.35

  next_Color[0] = Normalization_Hue(next_Color[0])
  next_Color[1] = Normalization_Saturaton_or_Lightness(next_Color[1])
  next_Color[2] = Normalization_Saturaton_or_Lightness(next_Color[2])

  return next_Color

def ComplexColor(base_Color):
  # コンプレックス配色で初期個体作成
  next_Color = [0.0, 0.0, 0.0]
  # 彩度の決定
  if (0<= base_Color[1] < 0.05) or (0<= base_Color[2] < 0.15):
    # 無彩色の場合
    rnd = random.uniform(0.0, 1.0)
    next_Color[1] = rnd
  else:
    next_Color[1] = base_Color[1]

  diff_Base = math.fabs(base_Color[0] - Hue_Yellow)
  n = 0
  if 0.7 < base_Color[2] < 1.0:
    if 0.33 <= base_Color[0] < 0.83:
      n = -2
    else:
      n = 2
  elif 0.0 < base_Color[2] < 0.3:
    if 0.33 <= base_Color[0] < 0.83:
      n = 2
    else:
      n = -2
  else:
    rnd = random.randint(0, 1)
    if rnd == 0:
      n = -2
    elif rnd == 1:
      n = 2

  H_Assort = base_Color[0] + n*0.04
  diff_Assort = math.fabs(H_Assort - Hue_Yellow)

  next_Color[0] = H_Assort
  if diff_Base < diff_Assort:
    next_Color[2] = base_Color[2] - 0.35
  else:
    next_Color[2] = base_Color[2] + 0.35

  next_Color[0] = Normalization_Hue(next_Color[0])
  next_Color[1] = Normalization_Saturaton_or_Lightness(next_Color[1])
  next_Color[2] = Normalization_Saturaton_or_Lightness(next_Color[2])

  return next_Color

def Guradetion_Color(base_color):
  # グラデーション配色
  next_Color = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  rnd_gradetion_number = random.uniform(0, 3)
  if 0.0<=rnd_gradetion_number<1.0:
    # 色相でのグラデーション配色
    next_Color[0] = base_color[0] + random.uniform(1, 3) * 0.04
    next_Color[1] = base_color[1]
    next_Color[2] = base_color[2]
    next_Color[3] = base_color[0] - random.uniform(1, 3) * 0.04
    next_Color[4] = base_color[1]
    next_Color[5] = base_color[2]
  elif 1.0<=rnd_gradetion_number<2.0:
    next_Color[0] = base_color[0]
    next_Color[1] = base_color[1] + random.uniform(1, 5) * 0.04
    next_Color[2] = base_color[2]
    next_Color[3] = base_color[0]
    next_Color[4] = base_color[1] - random.uniform(1, 5) * 0.04
    next_Color[5] = base_color[2]
  elif 2.0<=rnd_gradetion_number<=3.0:
    next_Color[0] = base_color[0]
    next_Color[1] = base_color[1]
    next_Color[2] = base_color[2] + random.uniform(1, 5) * 0.04
    next_Color[3] = base_color[0]
    next_Color[4] = base_color[1]
    next_Color[5] = base_color[2] - random.uniform(1, 5) * 0.04

  return next_Color


def Faux_Camaieu_Color(base_color):
  # フォカマイユ配色の関数
  next_Color = [0.0, 0.0, 0.0]
  H_rnd = random.randint(-2, 2)
  SV_rnd = random.randint(0, 3)
  SV_rnd_positive_value = random.uniform(1, 10)
  SV_rnd_negative_value = random.uniform(-10, -1)

  next_Color[0] = base_color[0] + H_rnd * 0.04
  if H_rnd == 0:
    if SV_rnd == 0:
      next_Color[1] = base_color[1] + SV_rnd_positive_value*0.01
      next_Color[2] = base_color[2]
    elif SV_rnd == 1:
      next_Color[1] = base_color[1] + SV_rnd_negative_value*0.01
      next_Color[2] = base_color[2]
    if SV_rnd == 2:
      next_Color[2] = base_color[2] + SV_rnd_positive_value*0.01
      next_Color[1] = base_color[1]
    elif SV_rnd == 3:
      next_Color[2] = base_color[2] + SV_rnd_negative_value*0.01
      next_Color[1] = base_color[1]
  else:
    next_Color[1] = base_color[1]
    next_Color[2] = base_color[2]

  next_Color[0] = Normalization_Hue(next_Color[0])
  next_Color[1] = Normalization_Saturaton_or_Lightness(next_Color[1])
  next_Color[2] = Normalization_Saturaton_or_Lightness(next_Color[2])

  return next_Color

def ToneOnToneColor(base_Color):
  # トーンオントーン配色の関数
  next_Color = [0.0, 0.0, 0.0]
  next_Color[0] = base_Color[0]

  SV_rnd = random.randint(0, 1)
  SV_value_rnd = random.uniform(-0.75, 0.75)

  if SV_rnd == 0:
    next_Color[1] = base_Color[1] + SV_value_rnd
    next_Color[2] = base_Color[2]
  elif SV_rnd == 1:
    next_Color[2] = base_Color[2] + SV_value_rnd
    next_Color[1] = base_Color[1]

  next_Color[0] = Normalization_Hue(next_Color[0])
  next_Color[1] = Normalization_Saturaton_or_Lightness(next_Color[1])
  next_Color[2] = Normalization_Saturaton_or_Lightness(next_Color[2])

  return next_Color

def ToneInToneColor(base_Color):
  # トーンイントーン配色の関数
  next_Color = [0.0, 0.0, 0.0]
  H_rnd = random.uniform(0, 25)
  next_Color[0] = H_rnd * 0.04

  SV_rnd = random.randint(0, 1)
  SV_value_rnd = random.uniform(-0.1, 0.1)

  if SV_rnd == 0:
    next_Color[1] = base_Color[1] + SV_value_rnd
    next_Color[2] = base_Color[2]
  elif SV_rnd == 1:
    next_Color[2] = base_Color[2] + SV_value_rnd
    next_Color[1] = base_Color[1]

  next_Color[0] = Normalization_Hue(next_Color[0])
  next_Color[1] = Normalization_Saturaton_or_Lightness(next_Color[1])
  next_Color[2] = Normalization_Saturaton_or_Lightness(next_Color[2])

  return next_Color

def Tricolor(base_color):
  # トリコロール配色の関数
  next_Color = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  if base_color[1] < 0.05:
    # 無彩色の場合
    next_Color[0] = random.uniform(0.0, 1.0)
    next_Color[1] = random.uniform(0.5, 1.0)
    next_Color[2] = random.uniform(0.5, 1.0)
    next_Color[3] = random.uniform(0.0, 1.0)
    next_Color[4] = random.uniform(0.5, 1.0)
    next_Color[5] = random.uniform(0.5, 1.0)
  else:
    # 有彩色の場合
    selectrnd = random.randint(0,1)
    if selectrnd == 0:
      next_Color[0] = random.uniform(0.0, 1.0)
      next_Color[1] = 0.0
      next_Color[2] = random.uniform(0.0, 1.0)
      next_Color[3] = random.uniform(0.0, 1.0)
      next_Color[4] = random.uniform(0.5, 1.0)
      next_Color[5] = random.uniform(0.5, 1.0)
    else:
      next_Color[0] = random.uniform(0.0, 1.0)
      next_Color[1] = random.uniform(0.5, 1.0)
      next_Color[2] = random.uniform(0.5, 1.0)
      next_Color[3] = random.uniform(0.0, 1.0)
      next_Color[4] = 0.0
      next_Color[5] = random.uniform(0.0, 1.0)
  next_Color[0] = Normalization_Hue(next_Color[0])
  next_Color[1] = Normalization_Saturaton_or_Lightness(next_Color[1])
  next_Color[2] = Normalization_Saturaton_or_Lightness(next_Color[2])
  next_Color[3] = Normalization_Hue(next_Color[3])
  next_Color[4] = Normalization_Saturaton_or_Lightness(next_Color[4])
  next_Color[5] = Normalization_Saturaton_or_Lightness(next_Color[5])

  return next_Color

def Split_Complementary_Color(base_color):
  # スプリッド・コンプリメンタリー配色の関数
  next_Color = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  if base_color[1] < 0.05:
    rnd1 = random.uniform(0.0, 1.0)
    next_Color[0] = rnd1 + 0.4
    next_Color[3] = rnd1 + 0.58
    rnd1 = random.uniform(0.3, 1.0)
    next_Color[1] = rnd1
    next_Color[4] = rnd1
    next_Color[2] = base_color[2]
    next_Color[5] = base_color[2]
  else:
    next_Color[0] = base_color[0] + 0.4
    next_Color[3] = base_color[0] + 0.58
    next_Color[1] = base_color[1]
    next_Color[4] = base_color[1]
    next_Color[2] = base_color[2]
    next_Color[5] = base_color[2]
  next_Color[0] = Normalization_Hue(next_Color[0])
  next_Color[1] = Normalization_Saturaton_or_Lightness(next_Color[1])
  next_Color[2] = Normalization_Saturaton_or_Lightness(next_Color[2])
  next_Color[3] = Normalization_Hue(next_Color[3])
  next_Color[4] = Normalization_Saturaton_or_Lightness(next_Color[4])
  next_Color[5] = Normalization_Saturaton_or_Lightness(next_Color[5])

  return next_Color

def Triad(base_color):
  # トライアド配色の関数
  next_Color = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  if base_color[1] < 0.05:
    rnd1 = random.uniform(0.0, 1.0)
    next_Color[0] = rnd1 + 0.33
    next_Color[3] = rnd1 + 0.67
    rnd1 = random.uniform(0.3, 1.0)
    next_Color[1] = rnd1
    next_Color[4] = rnd1
    next_Color[2] = base_color[2]
    next_Color[5] = base_color[2]
  else:
    next_Color[0] = base_color[0] + 0.33
    next_Color[3] = base_color[0] + 0.67
    next_Color[1] = base_color[1]
    next_Color[4] = base_color[1]
    next_Color[2] = base_color[2]
    next_Color[5] = base_color[2]
  next_Color[0] = Normalization_Hue(next_Color[0])
  next_Color[1] = Normalization_Saturaton_or_Lightness(next_Color[1])
  next_Color[2] = Normalization_Saturaton_or_Lightness(next_Color[2])
  next_Color[3] = Normalization_Hue(next_Color[3])
  next_Color[4] = Normalization_Saturaton_or_Lightness(next_Color[4])
  next_Color[5] = Normalization_Saturaton_or_Lightness(next_Color[5])

  return next_Color

def MutantColor2(mu_color, Tabu_color):
  # タブー手法のみの差分進化
  F = 0.5
  rnd4 = -1.0
  rnd5 = -1.0
  CR = 1.0
  mutant_color = [] #子個体を入れる配列
  tabu_count = 0
  save_pos = []
  for i, agent in enumerate(mu_color):
    tabu_switch = 1
    pos = agent
    escape_count = 0
    while tabu_switch == 1:
      # i番目を含まない3個体をランダム選択
      rnd1, rnd2, rnd3 = random.sample([j for j in range(len(mu_color)) if j != i ], 3)
      # print("i=", i,"rnd1=", rnd1, "rnd2=", rnd2, "rnd3=", rnd3)
      rnd_select = random.uniform(0.0, 1.0)

      # ３個体から変異ベクトルを作成
      # if r_select_parcent > rnd_select:
      #   pos1 = r_color[rnd1]
      #   r_switch_num = 0
      # else:
      #   pos1 = mu_color[rnd1]
      #   r_switch_num = 1

      pos1 = mu_color[rnd1]
      pos2 = mu_color[rnd2]
      pos3 = mu_color[rnd3]
      # 要素ごとに計算出来るようにnumpy形式に変更
      pos1 = np.array(pos1)
      pos2 = np.array(pos2)
      pos3 = np.array(pos3)
      # 変異ベクトル作成
      # print("pos1=", pos1,"pos2=", pos2, "pos3=", pos3)
      m_pos = pos1 + F*(pos2 - pos3)
      # print("m_pos=", m_pos)
      # 変異ベクトルと交叉させて子個体を作成
      ri = random.randint(0, len(pos))
      # print("pos=", pos, ", m_pos=", m_pos)
      for j in range(len(pos)):
        if j == ri or random.uniform(0.0, 10.0) > CR:
          pos[j] = m_pos[j]
        else:
          pass

      # 正規化
      for i in range(len(pos)):
        if i % 3 == 0:
          # 色相の場合
          while pos[i] > 1.0 or pos[i] < 0.0:
            if pos[i] > 1.0:
              pos[i] -= 1.0
            elif pos[i] < 0.0:
              pos[i] += 1.0
        else:
          # 彩度，明度の場合
          while pos[i] > 1.0 or pos[i] < 0.0:
            if pos[i] > 1.0:
              pos[i] = 1.0 - (pos[i] - 1.0)
            elif pos[i] < 0.0:
              pos[i] *= -1.0

      # タブー個体の近くに生成されていないかの判定
      # pos_np_array = np.array(pos)
      tabu_for_switch = 0
      for agent in (Tabu_color):
        # tabu_color_np_array = np.array(agent)
        color_dis1 = get_dis_ciede2000(pos[0], pos[1], pos[2], agent[0], agent[1], agent[2])
        color_dis2 = get_dis_ciede2000(pos[3], pos[4], pos[5], agent[3], agent[4], agent[5])
        tabu_dis = (color_dis1+color_dis2)/2
        if color_dis1 < 7.0 and color_dis2 < 7.0:
          tabu_for_switch = 1

      if tabu_for_switch == 1:
        tabu_count += 1
        escape_count += 1

      if tabu_for_switch == 0 or escape_count > 20:
        tabu_switch = 0
        save_pos = copy.deepcopy(pos)
        # print("save_pos=", save_pos)

    mutant_color.append(save_pos)

  # print("new_color=", new_color)
  return mutant_color, tabu_count

def color_individual_distance(mu_color):
  # 個体間距離が10以下なら0を返し、10より大きければ1を返す関数
  individual_color = np.array(mu_color)
  for i in range(0, len(individual_color)):
    discrimination_dis = []
    for j in range(0, len(individual_color)):
      color_dis1 = get_dis_ciede2000(individual_color[i][0], individual_color[i][1], individual_color[i][2], individual_color[j][0], individual_color[j][1], individual_color[j][2])
      color_dis2 = get_dis_ciede2000(individual_color[i][3], individual_color[i][4], individual_color[i][5], individual_color[j][3], individual_color[j][4], individual_color[j][5])
      discrimination_dis.append((color_dis1+color_dis2)/2)
    if sum(discrimination_dis)/ len(discrimination_dis) > 10.0:
      return 1
  return 0

# Commented out IPython magic to ensure Python compatibility.
# 疑似ユーザ実験(一般的な差分進化)
from IPython.core.display import Math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import time
import copy
import math
import pandas as pd
import glob
from google.colab import drive

drive.mount('/content/drive')
# %matplotlib inline
# random.seed(10)

sum_number = 0 #試行回数をカウントする変数
sum_ave = [] #試行回数分の平均をとった目標個体との各個体の平均距離を入れる配列
sum_best = [] #試行回数分の平均をとった目標個体との各個体の最小距離を入れる配列
sum_tabu = [] #試行回数分の平均をとったタブー個体の回数を入れる配列
rnd_Number = 0 #試行回数を入れる変数
rnd_length = 50 #試行回数の上限を入れる変数
d_sum = []

while rnd_Number < rnd_length:
  final_generation = 50 # 最終世代数
  # 型_Colorは[色相，　彩度，　明度]の配列
  # 今回はアウターの色が決まっている場合
  base_Color=[0.5, 0.25, 0.5]  # アウターの色を入れる配列
  # itemImageNumber = random.randint(0, 11) # イメージ語の種類を入れる
  itemImageNumber = 1 #選択する印象番号を入れる変数
  de_color = [] # 個体集団を入れる配列
  # new_color = [] # 子個体集団を入れる配列
  answer_color = [0.42, 0.25, 0.5, 0.54, 0.25, 0.5]
  np_answer_color = np.array(answer_color)
  ave_dis = [] #各世代の平均距離を保存する配列
  best_dis = [] #各世代の最小距離を保存する配列
  tabu_count = [] #タブーが使われた回数をカウントする変数
  random.seed(rnd_Number) #randomの乱数のSeedを合わせる
  np.random.seed(rnd_Number) #numpyの乱数のSeedを合わせる
  d = []

  if (1<= itemImageNumber <= 3) or (7 <= itemImageNumber <= 10) or itemImageNumber == 5:
    # ナチュラル配色の初期個体生成
    color1 = NaturalColor(base_Color)
    color1.extend(NaturalColor(color1))
    de_color.append(color1)

    # グラデーション配色
    de_color.append(Guradetion_Color(base_Color))

    # フォカマイユ配色の初期個体生成
    color2 = Faux_Camaieu_Color(base_Color)
    color2.extend(Faux_Camaieu_Color(color2))
    de_color.append(color2)

    # トーンオントーン配色の初期個体生成
    color3 = ToneOnToneColor(base_Color)
    color3.extend(ToneOnToneColor(color3))
    de_color.append(color3)

    # トーンイントーン配色の初期個体生成
    color4 = ToneInToneColor(base_Color)
    color4.extend(ToneInToneColor(color4))
    de_color.append(color4)

    # トライアド配色の初期個体生成
    de_color.append(Triad(base_Color))


  else:
    # コンプレックス配色の初期個体生成
    color1 = ComplexColor(base_Color)
    color1.extend(ComplexColor(color1))
    de_color.append(color1)

    # トーンオントーン配色の初期個体生成
    color2 = ToneOnToneColor(base_Color)
    color2.extend(ToneOnToneColor(color2))
    de_color.append(color2)

    # トーンイントーン配色の初期個体生成
    color3 = ToneInToneColor(base_Color)
    color3.extend(ToneInToneColor(color3))
    de_color.append(color3)

    # スプリッド・コンプリメンタリー配色の初期個体生成
    de_color.append(Split_Complementary_Color(base_Color))

    # トライアド配色の初期個体生成
    de_color.append(Triad(base_Color))

    # トリコロール配色の初期個体生成
    de_color.append(Tricolor(base_Color))

  # print("base_color=", base_Color)
  # print("de_color=", de_color)
  dis_individual_sum = 0.0
  dis_individual = []
  # 目標個体との距離導出
  for j, agent in enumerate(de_color):
    np_de_color = np.array(agent)
    color_dis1 = get_dis_ciede2000(de_color[j][0], de_color[j][1], de_color[j][2], np_answer_color[0], np_answer_color[1], np_answer_color[2])
    color_dis2 = get_dis_ciede2000(de_color[j][3], de_color[j][4], de_color[j][5], np_answer_color[3], np_answer_color[4], np_answer_color[5])
    dis_individual.append((color_dis1+color_dis2)/2)  #各個体距離を追加

  d_kari = 0.0
  for j, agent in enumerate(de_color):
    color_dis1 = get_dis_ciede2000(de_color[0][0], de_color[0][1], de_color[0][2], de_color[j][0], de_color[j][1], de_color[j][2])
    color_dis2 = get_dis_ciede2000(de_color[0][3], de_color[0][4], de_color[0][5], de_color[j][3], de_color[j][4], de_color[j][5])
    d_kari += (color_dis1+color_dis2)/2

  d.append(d_kari / (len(de_color) - 1))  #各個体距離を追加

  best_dis.append(min(dis_individual))
  ave_dis.append(sum(dis_individual) / len(de_color))
  tabu_count.append(0)
  # print(0,"番目のdis=", dis_individual_sum/len(de_color))

  # plot_de_color = np.array(de_color)
  # fig = plt.figure()
  # plt.xlim(0.0, 1.0)
  # plt.ylim(0.0, 1.0)
  # #散布図の作成
  # plt.scatter(answer_color[0], answer_color[1], s=40, c="yellow")
  # plt.scatter(plot_de_color[:, 0], plot_de_color[:, 1], s=40,c="red")
  # # 描画
  # plt.show()

  # 差分進化させた子個体を生成するスケール
  F = 0.5 #スケーリングファクタ
  rnd4 = -1.0
  rnd5 = -1.0
  CR = 0.1 #交叉率
  num=1
  Tabu_color = []

  while num < final_generation:
    # 差分進化させた子個体を生成する
    de_color_copy = copy.deepcopy(de_color) # deepcopyでde_colorのリスト複製
    new_color = []
    dis_individual = []
    tabu_save = 0
    r_switch = []
    # print("de_color=",de_color)
    if num == 1:
      new_color = MutantColor(de_color_copy)  #差分ベクトルを作成
    else:
      new_color, tabu_save = MutantColor2(de_color_copy, Tabu_color)  #タブー手法のみの差分進化


    tabu_count.append(tabu_save)

    # print("new_color=",new_color)
    # print("r_switch=",r_switch)

    np_de_color = np.array(de_color)
    np_new_color = np.array(new_color)


    # if num > 1:
    #   fig = plt.figure()
    #   plt.xlim(0.0, 1.0)
    #   plt.ylim(0.0, 1.0)
    #   Tabu_color_np_array = np.array(Tabu_color)
    #   print("tabu=", len(Tabu_color_np_array))
    #   #散布図の作成
    #   plt.scatter(Tabu_color_np_array[:, 0],  Tabu_color_np_array[:, 1], s=20,c="black")
    #   plt.scatter(np_de_color[:, 0], np_de_color[:, 1], s=20,c="red")
    #   plt.scatter(np_new_color[:, 0], np_new_color[:, 1], s=20,c="blue")
    #   plt.scatter(answer_color[0], answer_color[1], s=20, c="yellow")
    #   # 描画
    #   plt.show()
    # else:
    #   fig = plt.figure()
    #   plt.xlim(0.0, 1.0)
    #   plt.ylim(0.0, 1.0)
    #   #散布図の作成
    #   plt.scatter(np_de_color[:, 0], np_de_color[:, 1], s=20,c="red")
    #   plt.scatter(np_new_color[:, 0], np_new_color[:, 1], s=20,c="blue")
    #   plt.scatter(answer_color[0], answer_color[1], s=20, c="yellow")
    #   # 描画
    #   plt.show()

    # new_colorとanswer_colorの距離を導出して保存
    color_worst = []
    color_best = []

    for i, agent in enumerate(de_color):
      color_dis1 = get_dis_ciede2000(de_color[i][0], de_color[i][1], de_color[i][2], np_answer_color[0], np_answer_color[1], np_answer_color[2])
      color_dis2 = get_dis_ciede2000(de_color[i][3], de_color[i][4], de_color[i][5], np_answer_color[3], np_answer_color[4], np_answer_color[5])
      de_dist = (color_dis1+color_dis2)/2 #各親個体距離を追加
      color_dis1 = get_dis_ciede2000(new_color[i][0], new_color[i][1], new_color[i][2], np_answer_color[0], np_answer_color[1], np_answer_color[2])
      color_dis2 = get_dis_ciede2000(new_color[i][3], new_color[i][4], new_color[i][5], np_answer_color[3], np_answer_color[4], np_answer_color[5])
      new_dist = ((color_dis1+color_dis2)/2)  #各子個体距離を追加
      # print("de_dist=", de_dist, "new_dist=", new_dist)
      if new_dist < de_dist:
        # new_color(差分ベクトル)の距離がde_color(ターゲットベクトル)よりも良い時に置き換える
        color_best.append(new_color[i])
        color_worst.append(de_color[i])
        de_color[i] = new_color[i]
      else:
        color_worst.append(new_color[i])
        color_best.append(de_color[i])

    # タブーに保存
    for worst in color_worst:
      if color_individual_distance(de_color) == 1:
        Tabu_color.append(worst)
        # print("Tabu_color=", Tabu_color)
    # print("de_color", num, "=",de_color)
    # alfa = np.random.normal(loc=1.0, scale=0.25, size=None)
    color_worst_np_array = np.array(color_worst)
    color_best_np_array = np.array(color_best)

    for j, agent in enumerate(de_color):
      np_de_color = np.array(agent)
      color_dis1 = get_dis_ciede2000(de_color[j][0], de_color[j][1], de_color[j][2], np_answer_color[0], np_answer_color[1], np_answer_color[2])
      color_dis2 = get_dis_ciede2000(de_color[j][3], de_color[j][4], de_color[j][5], np_answer_color[3], np_answer_color[4], np_answer_color[5])
      dis_individual.append((color_dis1+color_dis2)/2)  #各個体距離を追加

    d_kari = 0.0
    for j, agent in enumerate(de_color):
      color_dis1 = get_dis_ciede2000(de_color[0][0], de_color[0][1], de_color[0][2], de_color[j][0], de_color[j][1], de_color[j][2])
      color_dis2 = get_dis_ciede2000(de_color[0][3], de_color[0][4], de_color[0][5], de_color[j][3], de_color[j][4], de_color[j][5])
      d_kari += (color_dis1+color_dis2)/2

    d.append(d_kari / (len(de_color) - 1))  #各個体距離を追加

    best_dis.append(min(dis_individual))
    ave_dis.append(sum(dis_individual) / len(de_color)) #各世代の平均距離を導出し，ave_disに入れる

    num = num+1

  # print("best_dis=", min(best_dis))

  if rnd_Number == 0:
    sum_best = copy.deepcopy(best_dis)
    sum_ave = copy.deepcopy(ave_dis)
    sum_tabu = copy.deepcopy(tabu_count)
    d_sum = copy.deepcopy(d)
  else:
    for i in range(len(best_dis)):
      sum_ave[i] += ave_dis[i]
      sum_best[i] += best_dis[i]
      sum_tabu[i] += tabu_count[i]
      d_sum[i] += d[i]

  rnd_Number += 1

# print("tabu_count=", tabu_count)
for i in range(len(sum_best)):
  # 試行回数の平均をそれぞれの配列に入れる
  sum_ave[i] /= rnd_length
  sum_best[i] /= rnd_length
  sum_tabu[i] /= rnd_length
  d_sum[i] /= rnd_length

dict = {'Average_Distance' : sum_ave,
        'Best_Distance' : sum_best,
        'Tabu' : sum_tabu,
        'd_individual' : d_sum}
dataframe = pd.DataFrame(dict)
display(dataframe)

dataframe.to_csv('/content/drive/MyDrive/疑似ユーザ実験/テスト実験結果(差分進化（タブーのみ_CIEDE2000)).csv', index = False)
# print(de_color)