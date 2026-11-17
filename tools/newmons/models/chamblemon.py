"""Chamblemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the mushroom bruiser. A round hot-pink body under a huge pale mushroom cap blushing pink, a sly grin
with buck teeth, pink arms and legs dotted with pale green spots, big black boxing gloves (one stamped with a pink
skull), and heavy black boots with buckles and green studs; a tiny mushroom sprout follows at its feet.
15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import leather, local, metal, mix, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a round hot-pink body under a huge pale mushroom cap, a sly buck-toothed grin, green-spotted limbs, big black "
        "boxing gloves and heavy black studded boots")
BASE = {"pink": (240, 80, 190), "pink_dark": (170, 30, 130), "cap": (240, 246, 220), "cap_pink": (240, 180, 210),
        "cap_dark": (190, 196, 170), "spot": (200, 240, 170), "black": (34, 32, 40), "black_light": (100, 98, 112),
        "tooth": (250, 240, 170), "eye": (40, 20, 30), "skull": (250, 120, 200), "steel": (200, 204, 216)}
SHINY = {"pink": (90, 160, 240), "pink_dark": (40, 90, 180), "cap_pink": (180, 210, 250), "skull": (120, 190, 250)}


def P(v):
    return pal(BASE, SHINY, v)


GLOVE = leather(P, "black", "black_light", stitch="steel")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.2) < 0.9 and abs(y - 24.4 - sx * 0.2) < 0.3:       # sly half-lidded eyes
                return tone(p["eye"], face), None
        if abs(y - 21.0 - 0.06 * x * x) < 0.25 and abs(x) < 4.0:
            return tone(p["eye"], face), None
        if 19.8 < y < 20.8 and 0.2 < abs(x) < 1.4:
            return tone(p["tooth"], face), None
    return skin(P, "pink", dark="pink_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def spottedf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if ((x * 1.3 + y * 0.7 + z) % 3.0) < 0.9 and ((y * 1.1 - z * 0.6) % 2.6) < 0.9:
        return tone(p["spot"], face), None
    return skin(P, "pink", dark="pink_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def capf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = max(0.0, min(1.0, (32.0 - y) / 4.0))
    col = mix(p["cap"], p["cap_pink"], t)
    if face == "down":
        col = p["cap_dark"]
    return tone(col, face), None


def gloveskull(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "west" and abs(z) < 1.4 and 9.6 < y < 12.6 and (abs(z) < 1.0 or y < 10.4):
        return tone(p["skull"], face), None
    return GLOVE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chamblemon")
    top = m.bone("chamblemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 22.0, 0), 7.6, bodyf, layers=6)
    hd = m.bone("head", bd, (0, 28, 0))
    for i, (r, y0, y1) in enumerate(((13.0, 28.0, 30.0), (12.4, 30.0, 33.0), (10.6, 33.0, 36.0), (7.6, 36.0, 38.4),
                                     (4.0, 38.4, 39.6))):
        m.round_box(hd, 0, 0, r, r * 0.92, y0, y1, capf, cut=max(1, round(r * 0.3)))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 24.0, 0))
        rod(m, ab, (sx * 7.0, 24.0, 0), (sx * 10.0, 16.0, -1.0), 2, spottedf, extend=0.4)
        m.round_box(ab, sx * 11.0, -1.4, 4.2, 4.2, 8.0, 16.0, gloveskull if sx < 0 else GLOVE, cut=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.6, 14.0, 0))
        rod(m, lg, (sx * 3.6, 15.0, 0), (sx * 4.0, 7.0, 0), 2, spottedf, extend=0.4)
        m.round_box(lg, sx * 4.4, -1.4, 3.6, 4.6, 0.0, 7.6, GLOVE, cut=1)              # heavy boots
        m.box(lg, sx * 4.4 - 3.7, 5.0, -4.0, sx * 4.4 + 3.7, 6.0, 1.4, solid(P, "steel"))
        for j in range(3):
            m.box(lg, sx * 8.0 - 0.6, 2.0, -2.6 + j * 2.0, sx * 8.0 + 0.6, 3.2, -1.4 + j * 2.0, solid(P, "spot"))
    kid = m.bone("sprout", top, (-9, 0, -6))                                       # the tiny mushroom follower
    m.round_box(kid, -9.0, -6.0, 1.4, 1.4, 0.0, 2.6, solid(P, "pink"), cut=1)
    m.round_box(kid, -9.0, -6.0, 2.4, 2.4, 2.6, 4.0, capf, cut=1)
    return m
