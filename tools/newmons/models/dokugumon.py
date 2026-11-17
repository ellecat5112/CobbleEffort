"""Dokugumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the poison spider. A hairy black spider with a great round black abdomen marked with a white skull
and crossbones, legs banded yellow and purple ending in red hooked tips, a fierce red face with a wild orange mane and
a beard, and a yellow-and-green dotted helmet with two curved horns. 15 blocks tall.

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fur, skin, solid, strands
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hairy black spider with a skull-and-crossbones abdomen, yellow-and-purple banded legs with red hooks, a red "
        "face with a wild orange mane and a horned yellow helmet")
BASE = {"black": (40, 38, 46), "black_dark": (10, 10, 14), "white": (240, 240, 244), "yellow": (240, 200, 50),
        "yellow_dark": (170, 120, 10), "green": (60, 160, 60), "purple": (100, 60, 150), "red": (210, 40, 40),
        "red_dark": (120, 10, 20), "mane": (230, 110, 40), "mane_dark": (150, 50, 10), "horn": (240, 230, 200),
        "eye": (250, 240, 120), "tooth": (250, 248, 240)}
SHINY = {"black": (110, 60, 140), "black_dark": (50, 20, 70), "red": (60, 140, 220), "red_dark": (20, 60, 140)}


def P(v):
    return pal(BASE, SHINY, v)


HAIR = fur(P, "black", "black_dark", length=1.4, density=2.0)


def abdf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "south"):
        a, b = (x, z - 10.0) if face == "up" else (x, y - 18.0)
        if math.hypot(a, b * 1.2) < 2.2 and not math.hypot(a * 1.6, b + 0.4) < 0.5:
            return tone(p["white"], face), None                         # skull
        if abs(abs(a) - abs(b)) < 0.5 and 2.0 < math.hypot(a, b) < 5.0:
            return tone(p["white"], face), None                         # crossbones
    return HAIR(x, y, z, face, variant, box=box, **k)


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (abs(x) + y) % 3.0
    return tone(p["yellow"] if t < 1.0 else p["purple"] if t < 1.6 else p["black"], face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.2) < 0.5 and abs(y - 11.6) < 0.3:
                return p["eye"], p["eye"]
        if abs(y - 9.4) < 0.4 and abs(x) < 1.6:
            return tone(p["tooth"] if (x * 2) % 1.0 < 0.5 else p["red_dark"], face), None
    return skin(P, "red", dark="red_dark")(x, y, z, face, variant, box=box, **k)


def helmf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (int(x * 1.2) + int(z * 1.2)) % 3 == 0 and face == "up":
        return tone(p["green"], face), None
    return armour(P, "yellow", "yellow_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dokugumon")
    top = m.bone("dokugumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 16.0, 10.0), 9.0, abdf, layers=7, squash=1.1)                      # great abdomen
    m.round_box(bd, 0, -2.0, 5.0, 5.0, 8.0, 15.0, HAIR, cut=2)                         # cephalothorax
    hd = m.bone("head", bd, (0, 12, -6))
    m.round_box(hd, 0, -7.0, 3.0, 2.0, 8.0, 14.0, facef, cut=1)                        # red face
    m.round_box(hd, 0, -6.0, 3.6, 2.6, 13.4, 16.0, helmf, cut=1)                       # dotted helmet
    for sx in (-1, 1):
        pts = [(sx * 3.4, 15.0, -6.0), (sx * 6.0, 16.0, -6.0), (sx * 7.0, 18.6, -7.0)]
        for p0, p1 in zip(pts, pts[1:]):                                               # curved horns
            rod(m, hd, p0, p1, 1, solid(P, "horn"), extend=0.4, t2=2)
    for i in range(14):                                                                # wild orange mane + beard
        ang = math.radians(-160 + i * 24)
        rod(m, hd, (3.6 * math.cos(ang), 11.0 + 3.6 * math.sin(ang), -6.0),
            (6.0 * math.cos(ang), 11.0 + 6.0 * math.sin(ang), -4.0), 1, strands(P, "mane", "mane_dark"), extend=0.3,
            t2=2)
    legs = [("leg_front_left", 1, -4.0), ("leg_front_right", -1, -4.0), ("leg_back_left", 1, 2.0),
            ("leg_back_right", -1, 2.0)]
    for nm, sx, z in legs:                                                             # eight legs, two per bone
        lg = m.bone(nm, bd, (sx * 4.0, 10.0, z))
        for k_ in range(2):
            zz = z + k_ * 3.0
            pts = [(sx * 4.0, 10.0, zz), (sx * 10.0, 14.0, zz + (zz * 0.3)), (sx * 15.0, 6.0, zz * 1.4),
                   (sx * 16.0, 1.0, zz * 1.5)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, lg, p0, p1, 2, bandf, extend=0.5)
            spike(m, lg, pts[-1], (sx * 0.3, -1, 0), 1.2, 2.0, solid(P, "red"), tip=0.25)
    return m
