"""Ex-Tyranomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the stuffed-toy tyrant. A chubby pink plush tyrannosaur sewn together with purple stitches, a huge round head with an
enormous open mouth of white felt fangs and a glowing pair of eyes deep inside, a white tummy patch stitched with a
zigzag seam, button eyes on its head, green felt back plates, a stubby tail and big black claws on its paws and feet.
25 blocks tall.

Front is -z, y is up. 42 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 42
SCALE, HITBOX = sized(25, HEIGHT, 3.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a chubby pink plush tyrannosaur with purple stitches, an enormous felt-fanged mouth with glowing eyes inside, a "
        "stitched white tummy, button eyes, green felt plates and black claws")
BASE = {"pink": (240, 90, 140), "pink_dark": (170, 40, 90), "white": (246, 246, 246), "white_dark": (200, 200, 206),
        "stitch": (90, 50, 130), "black": (24, 22, 26), "mouth": (40, 10, 20), "glow": (250, 230, 120),
        "green": (90, 170, 80), "button": (200, 60, 60)}
SHINY = {"pink": (120, 180, 240), "pink_dark": (60, 110, 180)}


def P(v):
    return pal(BASE, SHINY, v)


PLUSH = fur(P, "pink", "pink_dark", length=0.6, density=3.0)


def stitchedf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west", "up") and abs((x * 0.8 + z * 0.6) % 7.0 - 3.5) < 0.18 and (y * 2) % 1.0 < 0.55:
        return tone(p["stitch"], face), None
    return PLUSH(x, y, z, face, variant, box=box, **k)


def tummyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x - 0.6 * math.sin(y * 1.6)) < 0.25:
        return tone(p["stitch"], face), None                           # zigzag seam
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 22.0 < y < 34.0 and abs(x) < 6.6 - (y - 28.0) ** 2 * 0.12:
        fang = abs((x * 0.55) % 2.0 - 1.0) * 3.0
        if y > 32.0 - fang or y < 24.0 + fang:
            return tone(p["white"], face), None
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.6, y - 29.0) < 0.7:
                return p["glow"], p["glow"]
        return tone(p["mouth"], face), None
    return stitchedf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("extyranomon")
    top = m.bone("extyranomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 15.0, 0), 8.0, stitchedf, layers=6, squash=0.9)
    m.round_box(bd, 0, -6.6, 4.6, 1.0, 9.0, 20.0, tummyf, cut=1)
    hd = m.bone("head", bd, (0, 23, -1))
    ball(m, hd, (0, 29.0, -1.0), 8.0, headf, layers=6, squash=0.85, ry=8.0)
    for sx in (-1, 1):                                                                 # button eyes
        m.round_box(hd, sx * 7.4, -1.0, 0.6, 1.6, 33.0, 36.0, solid(P, "button"), cut=0)
    for j in range(5):                                                                 # green felt back plates
        spike(m, bd, (0, 34.0 - j * 4.6, 6.0), (0, 0.4, 1), 2.6, 3.0, solid(P, "green"), tip=1.0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 18.0, -2.0))
        m.round_box(ab, sx * 10.0, -4.0, 3.0, 3.0, 13.0, 19.0, stitchedf, cut=1)
        for j in range(3):
            spike(m, ab, (sx * 10.0 + (j - 1) * 1.6, 13.0, -6.0), (0, -0.4, -1), 1.4, 4.0, solid(P, "black"), tip=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 8.0, 0))
        m.round_box(lg, sx * 5.0, -1.0, 3.6, 4.4, 0.0, 8.0, stitchedf, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 5.0 + (j - 1) * 2.0, 1.0, -5.0), (0, -0.2, -1), 1.4, 4.0, solid(P, "black"), tip=0.3)
    tl = m.bone("tail", bd, (0, 10, 7))
    rod(m, tl, (0, 10.0, 7.0), (4.0, 6.0, 13.0), 4, stitchedf, extend=0.6)
    return m
