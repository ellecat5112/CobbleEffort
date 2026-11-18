"""Noble Pumpmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the pumpkin aristocrat: a jack-o'-lantern head with a green stalk face and glowing eyes under a
tall navy top hat with goggles, a white tailored suit with gold buttons, a great navy cloak of shaggy feathers flaring
from its shoulders, white gloves, a slim cane, and thin legs floating over a dark ring of smoke. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import fabric, feathers, metal, skin, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a pumpkin aristocrat with a jack-o'-lantern head under a tall navy top hat, a white suit with gold buttons, a "
        "great navy feather cloak, white gloves and a slim cane")
BASE = {"pumpkin": (240, 130, 30), "pumpkin_dark": (170, 70, 10), "green": (90, 170, 60), "white": (240, 240, 246),
        "white_dark": (180, 184, 200), "navy": (40, 50, 110), "navy_dark": (14, 18, 50), "gold": (230, 190, 70),
        "glow": (255, 230, 90), "black": (30, 28, 34), "smoke": (90, 90, 100, 150)}
SHINY = {"pumpkin": (150, 90, 200), "pumpkin_dark": (80, 40, 130), "navy": (120, 30, 40), "navy_dark": (60, 10, 14)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT0 = fabric(P, "white", "white_dark")


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.5 and (y % 3.0) < 0.7:
        return tone(p["gold"], face), None
    return SUIT0(x, y, z, face, variant, box=box, **k)


def pumpf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and abs(((math.atan2(z, x) * 3.0) % 1.0) - 0.5) < 0.08:
        return tone(p["pumpkin_dark"], face), None
    return tone(p["pumpkin"], face), None


def build():
    m = Model("noblepumpmon")
    mats = {"skin": suitf, "neck": skin(P, "green", dark="navy_dark"), "hand": SUIT0, "finger": SUIT0}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.75, leg_bulk=0.7, name="noblepumpmon")
    bd = a["body"]
    cape(m, bd, 52.0, 26.0, 40.0, feathers(P, "navy", "navy_dark"), z=3.0, flare=1.6, panels=8, seed=6)
    for sx in (-1, 1):                                                                   # feather collar
        for j in range(4):
            spike(m, bd, (sx * (3.0 + j * 1.4), 52.0, 1.0), (sx * 0.8, 0.6, 0.4), 2.0, 6.0, feathers(P, "navy", "navy_dark"),
                  tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    ball(m, hd, (0, 58.6, 0), 4.0, pumpf, layers=5, ry=3.6)                                # jack-o'-lantern head
    for sx in (-1, 1):
        m.box(hd, sx * 1.6 - 0.8, 59.0, -4.05, sx * 1.6 + 0.8, 60.4, -3.9, solid(P, "glow", glow=True))
    m.box(hd, -2.0, 56.2, -4.0, 2.0, 57.2, -3.85, solid(P, "glow", glow=True))
    m.round_box(hd, 0, 0, 5.4, 5.0, 62.0, 62.8, solid(P, "navy"), cut=1)                  # top hat
    m.round_box(hd, 0, 0, 3.2, 3.0, 62.8, 68.6, fabric(P, "navy", "navy_dark"), cut=1)
    m.box(hd, -3.3, 63.4, -3.2, 3.3, 64.6, -2.9, metal(P, "gold"))                         # goggles band
    al = a["arm_left"]                                                                   # slim cane
    h = al["hand"]
    rod(m, al["bone"], (h[0], h[1], h[2] - 1.0), (h[0] + 1.0, h[1] - 22.0, h[2] - 4.0), 1, solid(P, "black"),
        extend=0.2)
    ball(m, al["bone"], (h[0], h[1] + 0.8, h[2] - 1.0), 0.9, metal(P, "gold"), layers=1)
    m.round_box(a["top"], 0, 0, 6.0, 6.0, 0.0, 0.6, solid(P, "smoke"), cut=2)             # smoke ring
    return m
