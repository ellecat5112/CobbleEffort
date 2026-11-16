"""Archnemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a spider-woman demon beast, in her official outfit. A slender upper body in a red long-sleeved suit
with white trim and pale gauntlet claws, white hair, small curled red horns and a pale painted face, set on the body
of a great spider: a round red abdomen banded in violet and eight long red legs wrapped in white bands with steel
tips. 25 blocks tall.

Front is -z, y is up. 46 units tall; Perfect stage. Official outfit only.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, local, metal, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 46
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a spider-woman demon beast: a slender upper body in a red suit with white trim and pale claws, white hair and "
        "curled red horns, on a great red spider body banded in violet with eight white-banded legs")
BASE = {"red": (200, 40, 50), "red_dark": (110, 14, 24), "red_light": (250, 120, 120), "violet": (120, 80, 170),
        "white": (246, 246, 250), "white_dark": (190, 194, 210), "skin": (240, 236, 236), "skin_dark": (190, 180, 190),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "lip": (180, 30, 60), "eye": (40, 30, 40)}
SHINY = {"red": (40, 40, 60), "red_dark": (14, 14, 24), "red_light": (110, 110, 140), "violet": (60, 170, 170)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = fabric(P, "red", "red_dark", axis="y", period=2.6)
HAIR = strands(P, "white", "white_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def abdomenf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    band = (b + z * 0.3) % 4.0
    if band < 1.2:
        return tone(p["violet"], face), None
    return armour(P, "red", "red_dark", light="red_light")(x, y, z, face, variant, box=box, **k)


def legf(x, y, z, face, variant, box=None, **k):
    """A red leg wrapped in crossing white bands."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = (box.lo[2] + box.size[2] - z) if box else 0
    if abs(((t + u * 0.6) % 3.0) - 1.5) < 0.35:
        return tone(p["white"], face), None
    return tone(p["red"], face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 0.8) < 0.45 and abs(y - 41.4) < 0.25:
                return p["eye"], None
        if abs(x) < 0.6 and abs(y - 39.6) < 0.25:
            return p["lip"], None
    return skin(P, "skin", dark="skin_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("archnemon")
    top = m.bone("archnemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 18.0, 6.0), 9.0, abdomenf, layers=7, squash=1.1)                    # spider abdomen
    ball(m, bd, (0, 17.0, -3.0), 4.6, abdomenf, layers=4)                               # cephalothorax
    up = m.bone("torso", bd, (0, 21, -4))                        # the woman's upper body rising from the front
    m.round_box(up, 0, -4.0, 2.6, 1.8, 21.0, 27.0, SUIT, cut=1)
    m.round_box(up, 0, -4.0, 3.0, 2.0, 27.0, 34.0, SUIT, cut=1)
    m.box(up, -3.2, 33.0, -6.2, 3.2, 34.6, -1.8, solid(P, "white"))                    # white collar trim
    m.round_box(up, 0, -4.0, 1.0, 1.0, 34.0, 36.0, skin(P, "skin"), cut=0.4)
    hd = m.bone("head", up, (0, 36, -4))
    m.round_box(hd, 0, -4.0, 2.0, 2.2, 36.0, 42.6, facef, cut=1)
    hr = m.bone("mane", hd, (0, 42, -3))
    for i in range(11):                                          # spiky white hair
        ang = math.radians(-100 + i * 20)
        rod(m, hr, (1.6 * math.sin(ang), 42.0, -4.0 + 1.6 * math.cos(ang) * 0.5),
            (4.6 * math.sin(ang), 39.0 + 2.0 * abs(math.cos(ang)), -2.0 + 2.6 * math.cos(ang)), 1, HAIR, extend=0.3)
    for sx in (-1, 1):                                           # curled red horns
        pts = [(sx * 1.4, 42.6, -4.0), (sx * 2.6, 45.0, -4.4), (sx * 3.6, 45.4, -3.4), (sx * 3.4, 44.0, -2.8)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # arms reaching forward, pale claw gauntlets
        ab = m.bone(nm, up, (sx * 3.2, 32.0, -4.0))
        el = (sx * 6.0, 27.0, -7.0)
        hand = (sx * 7.0, 24.0, -12.0)
        rod(m, ab, (sx * 3.2, 32.0, -4.0), el, 2, SUIT, extend=0.4)
        rod(m, ab, el, hand, 2, solid(P, "white"), extend=0.4)
        for f in range(4):
            spike(m, ab, hand, (sx * 0.2 + (f - 1.5) * 0.25, -0.4, -1), 0.8, 3.0, STEEL)
    for i in range(4):                                           # eight long banded legs
        zz = -4.0 + i * 3.0
        for sx in (1, -1):
            nm = f"leg_{i}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 4.0, 17.0, zz))
            knee = (sx * 13.0, 26.0 - i, zz - 3.0 + i * 2.0)
            foot = (sx * 18.0, 0.0, zz - 6.0 + i * 4.0)
            rod(m, lg, (sx * 4.0, 17.0, zz), knee, 2, legf, extend=0.5)
            rod(m, lg, knee, foot, 2, legf, extend=0.5)
            spike(m, lg, foot, (0, -1, 0), 1.0, 2.0, STEEL)
    return m
