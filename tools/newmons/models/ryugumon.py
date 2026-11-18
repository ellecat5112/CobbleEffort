"""Ryugumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the dragon-palace oarfish: a long serpentine body of starry blue and violet ringed with silver
bands, a slender pale crested head with long golden feelers, flowing translucent blue-white veil fins spotted with
light, pink-and-violet streamer ribbons, a jade-scaled palace shell riding on its back, and a frilled tail fan of
pink and gold. 35 blocks.

Front is -z, y is up. 58 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 58
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a long starry blue oarfish-dragon ringed with silver, with flowing veil fins, pink ribbons, a jade palace shell and golden feelers"
BASE = {"blue": (60, 90, 220), "blue_dark": (30, 30, 130), "star": (240, 250, 255), "silver": (210, 214, 226),
        "silver_dark": (110, 114, 130), "pale": (220, 236, 250), "gold": (240, 200, 90), "gold_dark": (160, 120, 30),
        "veil": (140, 210, 250, 170), "pink": (250, 110, 210), "jade": (60, 160, 140), "jade_dark": (20, 90, 80),
        "eye": (250, 80, 160)}
SHINY = {"blue": (200, 60, 120), "blue_dark": (110, 20, 60), "veil": (250, 190, 220, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if math.sin(x * 2.1 + y * 1.3) * math.sin(z * 1.7 - y) > 0.93:
        return p["star"], p["star"]
    return tone(p["blue"] if (x + y + z) % 6.0 < 4.0 else p["blue_dark"], face), None


def veilf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if math.sin(x * 1.3) * math.sin(y * 1.1) > 0.85:
        return p["star"][:3] + (220,), None
    return p["veil"], None


def build():
    m = Model("ryugumon")
    top = m.bone("ryugumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    pts = [(0, 42.0, -12.0), (0, 34.0, -8.0), (0, 26.0, -2.0), (4.0, 20.0, 6.0), (10.0, 18.0, 14.0), (12.0, 24.0, 22.0),
           (8.0, 30.0, 26.0), (2.0, 28.0, 30.0), (-2.0, 22.0, 32.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):                                     # serpentine body
        b = m.bone(f"coil_{i}", bd, p0)
        rod(m, b, p0, p1, max(3, 6 - i // 2), bodyf, extend=0.8)
        if i % 2 == 1:
            m.round_box(b, p1[0], p1[2], 3.6, 3.6, p1[1] - 0.6, p1[1] + 0.6, metal(P, "silver", dark="silver_dark"), cut=1)
    hd = m.bone("head", bd, pts[0])
    m.round_box(hd, 0, -15.0, 2.0, 3.6, 41.0, 46.0, solid(P, "pale"), cut=1)                # slender head
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.9, sx * 2.1), 44.0, -16.0, max(sx * 1.9, sx * 2.1), 44.8, -14.8, solid(P, "eye", glow=True))
        pts2 = [(sx * 1.0, 46.0, -14.0), (sx * 3.0, 54.0, -16.0), (sx * 6.0, 58.0, -10.0), (sx * 8.0, 52.0, -4.0)]
        for p0, p1 in zip(pts2, pts2[1:]):                                                # golden feelers
            rod(m, hd, p0, p1, 1, metal(P, "gold", dark="gold_dark"), extend=0.2, t2=1)
    spike(m, hd, (0, 46.0, -12.0), (0, 1, 0.6), 1.4, 5.0, solid(P, "pink"), tip=0.8)       # crest
    fb = m.bone("veils", bd, (0, 32, -6))                                                 # flowing veil fins
    for sx in (-1, 1):
        for j in range(2):
            x0, x1 = sorted((sx * 3.0, sx * (14.0 + j * 4.0)))
            m.box(fb, x0, 12.0 + j * 4.0, -6.0 + j * 3.0, x1, 34.0, -6.0 + j * 3.0, veilf,
                  rotation=(10, -sx * 15, sx * 10), pivot=(sx * 3.0, 32.0, -6.0))
        pts3 = [(sx * 2.0, 36.0, -8.0), (sx * 10.0, 30.0, -12.0), (sx * 18.0, 24.0, -10.0)]
        for p0, p1 in zip(pts3, pts3[1:]):                                                # pink ribbons
            rod(m, fb, p0, p1, 1, solid(P, "pink"), extend=0.2, t2=3)
    ball(m, "coil_3", (6.0, 26.0, 8.0), 6.0, scales(P, "jade", "jade_dark", size=1.6), layers=4, ry=4.0)   # palace shell
    m.box("coil_3", 3.0, 30.0, 6.0, 9.0, 32.0, 10.0, armour(P, "gold", "gold_dark"))
    spike(m, "coil_3", (6.0, 32.0, 8.0), (0, 1, 0), 2.0, 3.0, armour(P, "gold", "gold_dark"), tip=0.8)
    for j in range(6):                                                                   # frilled tail fan
        ang = math.radians(-60 + j * 24)
        spike(m, "coil_7", pts[-1], (math.sin(ang) * 0.6, math.cos(ang), 0.4), 1.8, 7.0,
              solid(P, "pink" if j % 2 else "gold"), tip=0.8)
    return m
