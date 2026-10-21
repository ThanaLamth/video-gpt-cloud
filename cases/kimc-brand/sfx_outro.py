#!/usr/bin/env python3
"""SFX  KimQ outro 6s  - warm resolve + shimmer + C-major close + typing clicks"""
import os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from sfx_palette import Score, air, glass, wood, sub

s = Score(dur=6.0, T60=1.6)
p = s.place

# warm sub pad entry
p(sub(55, 1.2), 0.08, 0.40, 0.0, 0.28)

# shimmer sweep  3 glass tones L to R
p(glass(880,  0.50), 0.62, 0.28, -0.25, 0.38)
p(glass(1047, 0.50), 0.74, 0.24,  0.00, 0.38)
p(glass(1319, 0.50), 0.88, 0.20,  0.25, 0.38)

# CTA arrival glass tap
p(glass(659, 0.70), 1.50, 0.34, 0.0, 0.44)

# sparkle constellation
p(glass(1175, 0.60), 2.84, 0.26, 0.0, 0.40)
p(glass(988,  0.50), 2.96, 0.22, 0.0, 0.36)

# ── typing clicks: sync với typeOn(t=2.55, cps=22) ───────────────────
TEXT = 'Facebook: KimQ  \u2022  contact@kimq.tech'
T_START = 2.55
CPS = 22
random.seed(99)
for i, ch in enumerate(TEXT):
    if ch in (' ', '\u2022'):
        continue                          # khoảng trắng / bullet = im lặng
    t_ch = T_START + i / CPS
    freq  = random.randint(162, 218)      # pitch tự nhiên, không đều
    gain  = 0.10 + random.random() * 0.06
    p(wood(freq, 0.07), t_ch, gain, 0.0, 0.03)

# final C-major resolve spread
p(glass(523, 0.90), 4.82, 0.40, 0.0, 0.52)
p(glass(659, 0.80), 4.92, 0.34, 0.0, 0.48)
p(glass(784, 0.80), 5.04, 0.28, 0.0, 0.46)

s.write("sfx_outro.wav")
