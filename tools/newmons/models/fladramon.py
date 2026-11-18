"""Fladramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of courage. A lean dragon-man in red armour painted with yellow flames,
a red dragon helm with a short horn and a long flame-patterned snout, blue bodysuit at the joints, golden gauntlets
with three long steel claws on each, red greaves with flame trim, and a short blue tail. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage (Armor).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean dragon-man in red armour painted with yellow flames, a red dragon helm with a horn, blue bodysuit, golden "
        "gauntlets with long steel claws, red greaves and a short blue tail")
BASE = {"red": (220, 40, 30), "red_dark": (130, 14, 10), "flame": (250, 210, 40), "blue": (60, 90, 200),
        "blue_dark": (24, 40, 120), "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "steel": (210, 214, 224),
        "steel_dark": (100, 104, 116), "eye": (60, 200, 90)}
SHINY = {"red": (40, 40, 50), "red_dark": (14, 14, 20), "flame": (80, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", trim="gold", trim_w=0.25)
BLUE = skin(P, "blue", dark="blue_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def flamef(x, y, z, face, variant, box=None, **k):
    """Red armour with yellow flame tongues rising from the bottom of each plate."""
    p = P(variant)
    if box is not None and face not in ("up", "down"):
        u, v, W, H = local(x, y, z, face, box)
        if v / max(H, 1e-6) < 0.35 + 0.25 * abs(((u * 0.7) % 2.0) - 1.0):
            return tone(p["flame"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fladramon")
    mats = {"skin": BLUE, "chest": flamef, "abs": BLUE, "pelvis": RED, "neck": BLUE, "deltoid": flamef,
            "upper_arm": BLUE, "forearm": GOLD, "hand": GOLD, "finger": GOLD, "thigh": BLUE, "knee": RED,
            "shin": flamef, "calf": flamef, "foot": RED, "toe": RED}
    a = humanoid(m, mats, bulk=0.88, arm_bulk=0.95, leg_bulk=0.95, name="fladramon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0.0, 2.6, 3.0, 53.6, 59.6, flamef, cut=1)                         # dragon helm
    m.round_box(hd, 0, -4.2, 1.6, 2.0, 54.0, 57.0, flamef, cut=1)                        # snout
    spike(m, hd, (0, 59.4, -2.0), (0, 1, 0.4), 1.6, 4.0, GOLD, tip=0.4)                  # horn
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 57.4, -3.1, max(sx * 1.0, sx * 2.4), 58.2, -2.9, solid(P, "eye"))
        spike(m, hd, (sx * 2.4, 58.0, 1.0), (sx * 0.3, 0.3, 1), 1.2, 4.0, RED, tip=0.3)  # swept fins
    for nm in ("arm_left", "arm_right"):                                                # three long claws
        hnd = a[nm]["hand"]
        sx = 1 if hnd[0] > 0 else -1
        for j in range(3):
            spike(m, a[nm]["bone"], (hnd[0] + (j - 1) * 0.8, hnd[1] + 3.0, hnd[2] - 1.0), (sx * 0.2, -0.3, -1), 0.8,
                  9.0, metal(P, "steel", dark="steel_dark"), tip=0.2)
    rod(m, bd, (0, 32.0, 3.0), (0, 26.0, 9.0), 2, BLUE, extend=0.4, t2=1)               # short tail
    return m
