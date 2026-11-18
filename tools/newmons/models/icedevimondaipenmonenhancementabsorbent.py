"""Ice Devimon Daipenmon Enhancement Absorbent (a Digimon of the CobbleEffort: Digital crossover; hand-built after the
official art on wikimon.net): Daipenmon after absorbing Ice Devimon's data: the plump violet penguin with a fanged
violet maw gaping across its white belly, heavy-lidded scowling eyes, a red cap with a blue button, a black belt with a
silver buckle, white-and-blue shoes and great tattered pale-violet devil wings. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage (no level on wikimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import cutout, leather, local, metal, noise2, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a plump violet penguin with a fanged maw across its white belly, scowling eyes, a red cap, a black belt and "
        "tattered pale-violet devil wings")
BASE = {"violet": (80, 60, 160), "violet_dark": (36, 24, 90), "violet_light": (150, 130, 220), "white": (250, 250, 252),
        "yellow": (250, 210, 50), "eye": (24, 24, 30), "lid": (60, 44, 130), "maw": (110, 60, 150),
        "tooth": (250, 250, 250), "red": (200, 40, 50), "red_dark": (120, 14, 20), "blue": (60, 90, 200),
        "black": (30, 30, 36), "black_dark": (10, 10, 14), "steel": (200, 204, 216), "steel_dark": (100, 104, 116),
        "membrane": (190, 180, 240), "membrane_dark": (120, 110, 200), "shoe": (230, 236, 250)}
SHINY = {"violet": (40, 130, 120), "violet_dark": (14, 70, 60), "violet_light": (120, 210, 190),
         "membrane": (170, 230, 220), "membrane_dark": (90, 170, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 3.0) < 1.4 and 27.4 < y < 28.6:
                return tone(p["lid"] if y > 28.0 or (sx * x) < 2.2 - (y - 27.4) else p["eye"], face), None
        if 15.0 < y < 23.0 and abs(x) < 5.6 - abs(y - 19.0) * 0.4:                 # fanged maw across the belly
            if y > 21.6 and (x + 6.0) % 2.0 < 1.0:
                return tone(p["tooth"], face), None
            return tone(p["maw"], face), None
        if y < 24.0 and abs(x) < 7.0 - max(0.0, (y - 16.0) * 0.4):
            return tone(p["white"], face), None
    return skin(P, "violet", dark="violet_dark", light="violet_light", var=0.03)(x, y, z, face, variant, box=box, **k)


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.12 * abs(math.sin(u * 0.9)) + 0.06 * noise2(u, 0.0, 3)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["membrane_dark"] if (u * 0.7 + v) % 5.0 < 0.8 else p["membrane"], face), None


def build():
    m = Model("icedevimondaipenmonenhancementabsorbent")
    top = m.bone("icedevimondaipenmonenhancementabsorbent", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 18.0, 0), 10.0, bodyf, layers=8, squash=1.0)
    m.round_box(bd, 0, 0, 7.0, 6.0, 26.0, 32.0, bodyf, cut=2)
    m.box(bd, -2.0, 24.0, -9.6, 2.0, 26.0, -6.0, solid(P, "yellow"))                   # beak
    m.round_box(bd, 0, 0, 10.2, 10.2, 11.0, 13.4, leather(P, "black", "black_dark"), cut=4)   # belt
    m.box(bd, -2.0, 10.6, -10.6, 2.0, 13.8, -10.0, metal(P, "steel", dark="steel_dark"))
    hd = m.bone("head", bd, (0, 32, 0))                                                 # red cap
    m.round_box(hd, 0, 0.6, 4.4, 4.4, 31.4, 34.4, solid(P, "red"), cut=2)
    m.round_box(hd, 0, -4.4, 3.4, 1.6, 31.4, 32.2, solid(P, "red_dark"), cut=1)
    m.round_box(hd, 0, 0.6, 0.8, 0.8, 34.4, 35.4, solid(P, "blue"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                 # white-and-blue shoes
        lg = m.bone(nm, top, (sx * 4.0, 4.0, 0))
        m.round_box(lg, sx * 4.4, -1.6, 2.8, 3.8, 0.0, 4.6, solid(P, "shoe"), cut=1)
        m.box(lg, sx * 4.4 - 2.9, 1.0, -5.5, sx * 4.4 + 2.9, 2.0, 2.3, solid(P, "blue"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.0, 18.0, 0))
        m.box(ab, min(sx * 8.0, sx * 13.0), 12.0, -1.6, max(sx * 8.0, sx * 13.0), 20.0, 1.6,
              skin(P, "violet", dark="violet_dark"), rotation=(0, 0, sx * 20), pivot=(sx * 9.0, 18.0, 0))
    for side in (1, -1):                                                                # tattered devil wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 26.0, 6.0))
        bat_wing(m, wb, (side * 5.0, 26.0, 6.0), 18.0, 26.0, 4, skin(P, "membrane_dark", dark="violet_dark"),
                 cutout(tatter, wingf), side=side, sweep=10)
    return m
