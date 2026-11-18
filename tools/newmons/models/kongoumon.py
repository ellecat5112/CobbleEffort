"""Kongoumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
diamond-hard guardian beetle: a squat golden insect with a horned golden head and red eyes, a long string of violet
prayer beads looped over its body, a white sash hung with a sutra scroll, six golden arms each gripping a three-pronged
vajra, and short taloned legs. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, gem, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a squat golden insect with a horned head, violet prayer beads, a sutra sash and six golden arms gripping vajras"
BASE = {"gold": (240, 200, 70), "gold_dark": (160, 120, 20), "gold_light": (255, 240, 170), "violet": (200, 120, 200),
        "violet_light": (250, 210, 250), "white": (246, 244, 236), "white_dark": (190, 186, 170), "red": (210, 40, 40),
        "black": (30, 28, 30)}
SHINY = {"gold": (220, 224, 236), "gold_dark": (120, 126, 146), "gold_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light")
MET = metal(P, "gold", dark="gold_dark", light="gold_light")


def scrollf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.8 and (y % 1.6) < 0.4:
        return tone(p["black"], face), None
    return fabric(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)


def vajra(m, bone, c):
    x, y, z = c
    rod(m, bone, (x, y - 5.0, z), (x, y + 5.0, z), 1, MET, extend=0, t2=1)
    for end in (-1, 1):
        for j in (-1, 0, 1):
            spike(m, bone, (x, y + end * 5.0, z), (j * 0.4, end, 0), 0.8, 2.4, MET, tip=0.8)


def build():
    m = Model("kongoumon")
    top = m.bone("kongoumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0.6, 7.0, 6.0, 8.0, 26.0, GOLD, cut=3)
    m.round_box(bd, 0, -5.8, 2.2, 0.5, 4.0, 18.0, scrollf, cut=0)                       # sutra scroll
    m.round_box(bd, 0, 0.6, 7.2, 6.2, 17.0, 19.0, fabric(P, "white", "white_dark"), cut=2)
    for i in range(14):                                                              # prayer beads
        ang = math.radians(-160 + i * 23)
        m.round_box(bd, 6.6 * math.cos(ang) * 0.9, -6.0 + 0.4 * abs(math.sin(ang)), 1.0, 1.0,
                    24.0 + 3.0 * math.sin(ang) - 1.0, 24.0 + 3.0 * math.sin(ang) + 1.0, gem(P, "violet", "violet_light", glow=False),
                    cut=0)
    hd = m.bone("head", bd, (0, 26, -2))
    m.round_box(hd, 0, -2.4, 3.6, 3.6, 25.4, 32.0, GOLD, cut=1)
    m.box(hd, -1.0, 28.6, -6.1, 1.0, 29.6, -5.9, solid(P, "red", glow=True))
    pts = [(0, 31.6, -3.0), (0, 36.0, -5.0), (2.0, 39.0, -3.0)]                       # horn
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 2 - j, GOLD, extend=0.4)
    for row, (y0, nm) in enumerate(((24.0, "arm"), (19.0, "arm2"), (14.0, "arm3"))):  # six arms
        for sx in (-1, 1):
            ab = m.bone("%s_%s" % (nm, "left" if sx > 0 else "right"), bd, (sx * 6.6, y0, 0))
            hand = (sx * 13.0, y0 + 6.0 - row * 2.0, -2.0)
            rod(m, ab, (sx * 6.6, y0, 0), hand, 2, GOLD, extend=0.4)
            m.round_box(ab, hand[0], hand[2], 1.4, 1.4, hand[1] - 1.4, hand[1] + 1.4, solid(P, "black"), cut=0)
            vajra(m, ab, hand)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 8.0, 0))
        rod(m, lg, (sx * 4.0, 9.0, 0), (sx * 5.0, 2.0, -1.0), 2, GOLD, extend=0.4)
        for j in range(2):
            spike(m, lg, (sx * 5.0 + (j - 0.5) * 1.6, 1.0, -1.0), (0, -0.4, -1), 1.2, 3.0, MET, tip=0.8)
    return m
