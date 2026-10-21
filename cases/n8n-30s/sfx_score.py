import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from sfx_palette import Score, air, glass, wood, sub, wobble

s = Score(dur=30.0, T60=1.0)
p = s.place

# sub(f, dur)  glass(f, dur, bright)  air(dur, f0, f1)  wood(f, dur)  wobble(f, dur)
# p(sound, t_start, gain, pan, fade_dur)

T_HOOK_IN  = 0.50
T_SHAKE    = 1.20
T_SLASH    = 2.50
T_AFTER    = 2.80
T_N8N      = 4.50
T_STAR     = 5.20
T_TAGLINE  = 6.50
T_NODES    = 9.50
T_ICONS    = 15.00
T_AI_GLOW  = 19.00
T_RESULT   = 23.00
T_OSS      = 26.50
T_CTA      = 28.50

# Ambient sub pad throughout
p(sub(30, 30.0),           0.0,           0.02, 0.0, 30.0)

# HOOK: clock ticks (tension)
for i in range(8):
    p(wood(320 - i*8, 0.06), T_HOOK_IN + i*0.22, 0.06 + (i%3)*0.01, 0.0, 0.04)

# Shake rattle
for i in range(6):
    p(wood(180 + i*20, 0.04), T_SHAKE + i*0.12, 0.04, 0.0, 0.03)

# Sub build into slash
p(sub(55, 0.6),            T_SLASH - 0.15, 0.18, 0.0, 0.5)
p(air(0.3, 200, 2400),     T_SLASH,        0.16, 0.0, 0.3)
p(glass(880, 1.0, 0.8),    T_SLASH + 0.1,  0.20, 0.0, 0.5)
p(glass(1108, 0.8, 0.6),   T_SLASH + 0.25, 0.15, 0.0, 0.4)
p(glass(660, 0.6, 0.5),    T_AFTER,        0.12, 0.0, 0.3)

# n8n brand reveal — ascending triad
p(sub(50, 0.8),             T_N8N - 0.05,  0.08, 0.0, 0.6)
p(glass(523, 0.8, 0.7),     T_N8N + 0.05,  0.14, 0.0, 0.5)
p(glass(659, 0.7, 0.6),     T_N8N + 0.2,   0.12, 0.0, 0.4)
p(glass(783, 0.6, 0.5),     T_N8N + 0.35,  0.10, 0.0, 0.35)

# Star odometer sweep + ding at peak
p(air(1.2, 300, 1800),      T_STAR,        0.06, 0.0, 1.2)
p(glass(1047, 0.5, 0.4),    T_STAR + 1.1,  0.14, 0.0, 0.4)

# Tagline
p(glass(392, 0.5, 0.4),     T_TAGLINE + 0.1, 0.08, 0.0, 0.3)
p(glass(494, 0.5, 0.4),     T_TAGLINE + 0.4, 0.07, 0.0, 0.3)

# Workflow nodes — each node pops with a tone
node_tones = [330, 415, 523, 392, 494]
for i in range(5):
    t_node = T_NODES + 0.35 + i * 0.38
    p(glass(node_tones[i], 0.5, 0.4), t_node, 0.10, 0.0, 0.25)
    p(air(0.12, 200, 1000),            t_node + 0.08, 0.03, 0.0, 0.1)

# Icons grid cascade
for i in range(8):
    p(glass(350 + i*28, 0.35, 0.3), T_ICONS + 0.2 + i*0.09, 0.07, 0.0, 0.15)

# AI node glow — special warm swell
p(sub(45, 1.5),              T_AI_GLOW,       0.10, 0.0, 1.5)
p(glass(880, 1.2, 1.0),      T_AI_GLOW + 0.2, 0.16, 0.0, 0.8)
p(glass(1108, 0.8, 0.6),     T_AI_GLOW + 0.5, 0.12, 0.0, 0.5)
p(wobble(220, 2.0),           T_AI_GLOW + 0.1, 0.06, 0.0, 2.0)

# Result reveal + checkmarks
p(sub(50, 0.8),               T_RESULT,        0.08, 0.0, 0.5)
p(glass(660, 0.7, 0.6),       T_RESULT + 0.05, 0.13, 0.0, 0.4)
for i in range(3):
    p(glass(523 + i*70, 0.4, 0.3), T_RESULT + 0.9 + i*0.25, 0.09, 0.0, 0.2)

# OSS tags
for i in range(3):
    p(glass(440 + i*55, 0.4, 0.3), T_OSS + i*0.2 + 0.05, 0.07, 0.0, 0.2)

# CTA — triumphant finish
p(sub(45, 1.0),               T_CTA - 0.1,   0.12, 0.0, 1.0)
p(glass(880, 1.0, 0.8),       T_CTA + 0.1,   0.18, 0.0, 0.6)
p(glass(1109, 0.8, 0.6),      T_CTA + 0.3,   0.14, 0.0, 0.5)
p(glass(1320, 0.6, 0.4),      T_CTA + 0.5,   0.10, 0.0, 0.4)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfx.wav')
s.write(out)
print(f'sfx.wav written -> {out}')