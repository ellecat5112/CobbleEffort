"""Tonosama Mamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the lord of the Mamemon: a big shiny silver ball head with goggling ringed eyes, pink
cheeks and a beaming mouth, an antenna stalk topped with a little golden smiling ball, a blue kimono jacket with a
red sash and pleated navy hakama, yellow gloved hands, one waving a folding fan, and cherry petals drifting round it.
35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fabric, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a big shiny silver ball head with goggling eyes and a beaming mouth, a golden antenna ball, a blue kimono with navy hakama and a folding fan"
BASE = {"silver": (220, 224, 234), "silver_dark": (130, 134, 150), "blue": (60, 120, 200), "blue_dark": (24, 60, 130),
        "navy": (40, 50, 110), "navy_dark": (16, 20, 60), "red": (210, 40, 50), "yellow": (250, 210, 60),
        "yellow_dark": (200, 150, 20), "eye": (90, 140, 220), "pupil": (20, 20, 40), "white": (255, 255, 255),
        "pink": (250, 140, 170), "mouth": (200, 50, 70), "black": (30, 30, 34), "petal": (250, 190, 210),
        "gold": (240, 200, 60), "fan": (250, 240, 230)}
SHINY = {"silver": (240, 210, 140), "silver_dark": (170, 130, 60), "blue": (180, 60, 120), "blue_dark": (110, 20, 70)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 3.0, b - 24.0)
            if d < 2.2:
                c = eye(p, a - sx * 3.0, b - 24.0, 1.2, "eye")
                return (c if c is not None else p["white"]), None
            if d < 2.6:
                return p["black"], None
            if math.hypot(a - sx * 5.4, b - 20.6) < 1.2:
                return p["pink"], None
        if 18.0 < b < 21.0 and abs(a) < 2.4 - (21.0 - b) * 0.5:
            return p["mouth"], None
    return metal(P, "silver", dark="silver_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tonosamamamemon")
    top = m.bone("tonosamamamemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 6.6, 5.6, 0.0, 9.0, fabric(P, "navy", "navy_dark", axis="x", period=1.6), cut=2)  # hakama
    m.round_box(bd, 0, 0, 5.0, 4.0, 9.0, 15.0, fabric(P, "blue", "blue_dark"), cut=1)
    m.round_box(bd, 0, 0, 5.2, 4.2, 8.6, 10.0, solid(P, "red"), cut=1)
    hd = m.bone("head", bd, (0, 15, 0))
    ball(m, hd, (0, 23.0, 0), 8.4, headf, layers=6)
    rod(m, hd, (0, 31.0, 0), (0, 33.6, 1.0), 1, solid(P, "black"), extend=0.2)
    ball(m, hd, (0, 34.6, 1.0), 1.8, solid(P, "gold"), layers=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 13.0, 0))
        m.round_box(ab, sx * 6.6, -1.0, 2.0, 2.4, 9.0, 14.0, fabric(P, "blue", "blue_dark"), cut=1)
        ball(m, ab, (sx * 7.4, 8.0 if sx < 0 else 16.0, -2.6), 2.0, skin(P, "yellow", dark="yellow_dark"), layers=2)
    lb = m.bone("fan", bd, (7.4, 16, -2.6))                                            # folding fan
    for j in range(7):
        ang = (j - 3) * 0.28
        m.box(lb, 7.0, 17.0, -3.0, 7.8, 24.0, -2.8, solid(P, "fan" if j % 2 else "pink"),
              rotation=(0, 0, math.degrees(ang)), pivot=(7.4, 17.0, -2.9))
    pb = m.bone("petals", top, (0, 10, 0))
    for i in range(10):
        ang = i * 2 * math.pi / 10
        cx, cz = 13.0 * math.cos(ang), 13.0 * math.sin(ang)
        m.box(pb, cx - 0.9, 6.0 + (i * 7) % 20, cz - 0.6, cx + 0.9, 7.2 + (i * 7) % 20, cz + 0.6, solid(P, "petal"))
    return m
