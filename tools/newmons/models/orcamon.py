"""Orcamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of reliability: an orca-man with a sleek black body and white belly, a tall dorsal
fin tipped red rising from its head, flipper arms, a red-and-white life ring round its waist, an orange LIFE SAVER vest
with a red cross, and broad black flipper feet. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult (Armor) stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an orca-man with a sleek black body, a tall red-tipped dorsal fin, a red-and-white life ring and an orange life-saver vest"
BASE = {"black": (50, 52, 60), "black_dark": (18, 18, 24), "white": (240, 240, 246), "red": (220, 40, 40),
        "orange": (250, 170, 40), "orange_dark": (190, 110, 14), "eye": (60, 140, 90)}
SHINY = {"black": (60, 90, 170), "black_dark": (20, 40, 110)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "black", dark="black_dark")


def ringf(x, y, z, face, variant, box=None, **k):
    import math
    p = P(variant)
    return tone(p["red"] if (math.atan2(z, x) * 2.0 / math.pi) % 1.0 < 0.5 else p["white"], face), None


def vestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.0 and abs(y - 30.0) < 2.6 or (face == "north" and abs(y - 30.0) < 0.9 and abs(x) < 2.6):
        return tone(p["red"], face), None
    return fabric(P, "orange", "orange_dark")(x, y, z, face, variant, box=box, **k)


def build():
    import math
    m = Model("orcamon")
    top = m.bone("orcamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 22.0, 0.6), 7.0, HIDE, layers=6, ry=12.0)                              # sleek body
    ball(m, bd, (0, 20.0, -3.0), 5.0, skin(P, "white", dark="black_dark"), layers=4, ry=9.0, squash=0.5)
    m.round_box(bd, 0, -1.0, 6.0, 5.0, 26.0, 34.0, vestf, cut=1)                          # life-saver vest
    for i in range(12):                                                                  # life ring
        ang = 2 * math.pi * i / 12
        m.box(bd, 8.0 * math.cos(ang) - 1.6, 16.0, 8.0 * math.sin(ang) - 1.6, 8.0 * math.cos(ang) + 1.6, 19.2,
              8.0 * math.sin(ang) + 1.6, ringf)
    hd = m.bone("head", bd, (0, 34, 0))
    ball(m, hd, (0, 38.0, -1.0), 4.4, HIDE, layers=4, ry=4.0)
    m.round_box(hd, 0, -5.0, 2.4, 1.6, 35.0, 37.6, HIDE, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 2.0 - 0.8, 38.6, -4.4, sx * 2.0 + 0.8, 39.6, -4.2, solid(P, "white"))
        m.box(hd, sx * 2.0 - 0.3, 38.8, -4.45, sx * 2.0 + 0.3, 39.4, -4.4, solid(P, "eye"))
    spike(m, hd, (0, 41.0, 1.0), (0, 1, 0.5), 3.0, 9.0, HIDE, tip=0.8)                     # tall dorsal fin
    spike(m, hd, (0, 47.0, 4.0), (0, 1, 0.5), 1.4, 2.6, solid(P, "red"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # flipper arms
        ab = m.bone(nm, bd, (sx * 6.0, 28.0, 0))
        x0, x1 = sorted((sx * 6.0, sx * 14.0))
        m.box(ab, x0, 24.0, -1.0, x1, 29.0, 1.0, HIDE, rotation=(0, 0, -sx * 40), pivot=(sx * 6.0, 28.0, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 10.0, 0))
        rod(m, lg, (sx * 3.0, 11.0, 0), (sx * 3.4, 3.0, 0), 4, HIDE, extend=0.4)
        m.round_box(lg, sx * 4.0, -3.0, 3.0, 5.0, 0.0, 1.6, HIDE, cut=1)                  # broad flipper feet
    tb = m.bone("tail", bd, (0, 12, 6))
    rod(m, tb, (0, 12.0, 6.0), (0, 6.0, 12.0), 3, HIDE, extend=0.4)
    m.box(tb, -5.0, 5.0, 12.0, 5.0, 6.6, 16.0, HIDE)
    return m
