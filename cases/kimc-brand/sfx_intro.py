#!/usr/bin/env python3
"""SFX  KimC intro 3s  - ascending crystal triad + air whoosh + sub warmth"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from sfx_palette import Score, air, glass, wood, sub

s = Score(dur=3.0, T60=1.1)
p = s.place

# ascending crystal triad C5-E5-G5-B5  (pre-mark, mark, wordmark, slogan)
p(glass(523, 0.70),  0.06, 0.32, 0.0, 0.50)
p(glass(659, 0.70),  0.38, 0.28, 0.0, 0.50)
p(glass(784, 0.70),  0.78, 0.25, 0.0, 0.50)
p(glass(988, 0.80),  1.18, 0.22, 0.0, 0.50)

# soft air whoosh as mark pops in
p(air(0.35, 220, 2800), 0.42, 0.38, 0.0, 0.42)

# sub warmth  (body pulse)
p(sub(60, 0.70), 0.38, 0.34, 0.0, 0.22)

# wordmark sparkle
p(glass(1047, 0.50), 1.14, 0.22, 0.0, 0.40)

# resolve  G5 + E6
p(glass(784,  0.80), 2.40, 0.36, 0.0, 0.52)
p(glass(1319, 0.70), 2.52, 0.26, 0.0, 0.48)

s.write("sfx_intro.wav")
