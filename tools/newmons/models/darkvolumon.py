"""Dark Volumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the loudspeaker robot. A stocky navy machine whose whole chest is one great black loudspeaker cone,
a small boxy head with glowing yellow eyes under a gold vent, two tall hooked V antennae, spiked shoulders, big
clenched fists, a rotary six-barrel gatling gun on each arm, a gold belt grille and broad blocky feet. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage (no level known).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a stocky navy robot with a great black loudspeaker chest, glowing yellow eyes, hooked V antennae, spiked "
        "shoulders and a rotary gatling gun on each arm")
BASE = {"navy": (40, 54, 130), "navy_dark": (14, 20, 60), "navy_light": (100, 120, 210), "gold": (230, 180, 60),
        "gold_dark": (150, 100, 20), "black": (30, 30, 36), "cone": (50, 50, 58), "grey": (110, 110, 120),
        "grey_dark": (50, 50, 58), "eye": (250, 220, 40), "steel": (200, 204, 214), "steel_dark": (90, 94, 104)}
SHINY = {"navy": (150, 40, 50), "navy_dark": (70, 10, 20), "navy_light": (220, 110, 120)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "navy", "navy_dark", light="navy_light", rivets=True)
GOLD = metal(P, "gold", dark="gold_dark")
GUN = riveted(P, "grey", "grey_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def conef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    r = math.hypot(x, y - 30.0)
    if r < 1.2:
        return tone(p["grey"], face), None
    return tone(p["black"] if (r % 2.0) < 0.3 else p["cone"], face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.6) < 0.9 and abs(y - 41.6 + sx * 0.1 * (x - sx * 1.6)) < 0.4:
                return p["eye"], p["eye"]
    return HULL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("darkvolumon")
    top = m.bone("darkvolumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 0, 8.0, 5.4, 20.0, 39.0, HULL, cut=2)
    for i in range(5):                                                                   # the loudspeaker cone
        r = 7.0 - i * 1.3
        m.round_box(bd, 0, -5.0 - i * 0.3, r, 1.4, 30.0 - r, 30.0 + r, conef, cut=1)
    m.round_box(bd, 0, -0.6, 6.0, 4.4, 18.0, 21.0, GOLD, cut=1)                          # belt grille
    for j in range(4):
        m.box(bd, -3.0 + j * 1.8, 18.6, -5.2, -2.4 + j * 1.8, 20.4, -4.8, solid(P, "black"))
    hd = m.bone("head", bd, (0, 39, 0))
    m.round_box(hd, 0, -1.0, 3.4, 3.4, 39.0, 44.0, headf, cut=1)
    m.box(hd, -3.0, 44.0, -4.6, 3.0, 45.0, 2.0, GOLD)                                     # gold vent
    for j in range(4):
        m.box(hd, -2.6, 42.6, -4.6 + j * 1.4, 2.6, 44.0, -4.0 + j * 1.4, solid(P, "black"))
    for sx in (-1, 1):                                                                   # hooked V antennae
        p0, p1, p2 = (sx * 3.0, 44.0, 0), (sx * 11.0, 56.0, 0), (sx * 7.0, 58.0, 0)
        rod(m, hd, p0, p1, 2, HULL, extend=0.6)
        rod(m, hd, p1, p2, 2, HULL, extend=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.0, 35.0, 0))
        m.round_box(ab, sx * 10.0, 0, 3.4, 3.4, 33.0, 39.0, HULL, cut=1)                 # shoulder
        for j in range(3):
            spike(m, ab, (sx * 11.0, 38.0, -1.0 + j * 1.4), (sx * 0.4, 1, 0), 1.0, 3.0, STEEL)
        rod(m, ab, (sx * 11.0, 34.0, 0), (sx * 16.0, 26.0, 0), 3, HULL, extend=0.4)
        m.round_box(ab, sx * 18.0, -1.0, 3.6, 3.4, 19.0, 26.0, HULL, cut=1)               # fist
        gb = m.bone("spin_gun_" + ("left" if sx > 0 else "right"), ab, (sx * 12.0, 26.0, -4.0))
        m.round_box(gb, sx * 12.0, -4.0, 3.0, 3.0, 20.0, 22.0, GUN, cut=1)               # gatling drum
        for b in range(6):
            ang = b * math.pi / 3
            bx, bz = sx * 12.0 + 1.6 * math.cos(ang), -4.0 + 1.6 * math.sin(ang)
            rod(m, gb, (bx, 22.0, bz), (bx, 14.0, bz - 1.0), 1, GUN, extend=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 20.0, 0))
        rod(m, lg, (sx * 4.0, 20.0, 0), (sx * 6.0, 6.0, 0), 4, HULL, extend=0.4)
        m.box(lg, sx * 6.0 - 3.6, 0.0, -6.4, sx * 6.0 + 3.6, 4.0, 3.0, HULL)            # blocky feet
        m.box(lg, sx * 6.0 - 3.6, 0.0, -6.8, sx * 6.0 + 3.6, 1.0, -6.0, GOLD)
    return m
