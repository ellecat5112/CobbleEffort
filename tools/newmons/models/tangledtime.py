"""Tangled Time (Grass/Dragon), the ancient paradox Celebi, built from boxes after @goldmills_'s art (the art's own
name).

A wild little Celebi: a pale green head with mismatched eyes, one amber and ringed in red, one blue, the blue one half
hidden under a dark green tangle of vine across its face. Two red leaf-feather antennae and a white horn crown its
head, its body and legs are dark green ending in a ragged skirt of leaves, and its wings do not match: on one side a
long feather of red fading to orange and gold, on the other two small glassy blue wings.

Shiny: rose-pink head and a teal body, with a violet feather wing.

Front is -z, y is up. 30 units tall; about 1.0 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, stars
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 30
SCALE = round(1.0 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = ("a wild little Celebi with mismatched amber and blue eyes, a vine tangle across its face, red leaf antennae "
        "and a white horn, a ragged leafy skirt, one long red-to-gold feather wing and two small blue wings")

BASE = {"pale": (212, 236, 196), "pale_dark": (170, 206, 156), "green": (64, 114, 74), "green_dark": (40, 80, 50),
        "vine": (36, 70, 44), "red": (226, 70, 80), "orange": (250, 150, 70), "gold": (250, 214, 110),
        "amber": (250, 196, 60), "rim": (210, 40, 50), "blue": (110, 190, 230), "pupil": (30, 24, 30),
        "horn": (236, 238, 242), "wing_blue": (170, 220, 250, 200), "white": (255, 255, 255)}
SHINY = {"pale": (250, 200, 214), "pale_dark": (220, 160, 182), "green": (50, 130, 130), "green_dark": (30, 90, 94),
         "vine": (24, 70, 74), "red": (170, 90, 230), "orange": (220, 130, 250), "gold": (250, 200, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def headf(x, y, z, face, variant, **k):
    """Pale green; an amber eye ringed red on its left, a blue eye on its right half hidden under a dark vine."""
    p = P(variant)
    if face == "north":
        for sx, iris in ((-1, "amber"), (1, "blue")):
            dx, dy = x - sx * 1.9, y - 18.6
            e = (dx / 1.25) ** 2 + (dy / 1.45) ** 2
            if e < 1:
                if sx > 0 and dy > 0.3 + dx * 0.3:
                    return p["vine"], None                                      # the vine over its blue eye
                if math.hypot(dx, dy) < 0.5:
                    return p["pupil"], None
                return p[iris], None
            if e < 1.4 and sx < 0:
                return p["rim"], None
        if x > 0.6 and abs(y - (19.8 + (x - 0.6) * 0.5)) < 0.6:
            return p["vine"], None                                              # vine tangle across the face
    return lit(p["pale"], face, y, 18.0, 4), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.2 and y > 11.0:
        return tone(p["pale"], face), None
    return tone(p["green"], face), None


def featherf(x, y, z, face, variant, **k):
    """One long feather wing (an xy plane to its left): red at the root fading to orange and gold at the tip."""
    p = P(variant)
    u, v = x - 2.4, y - 14.0                                             # from the wing root
    L = math.hypot(u, v)
    ang = math.atan2(v, u)
    if not (0.35 < ang < 1.25) or L > 16.0:
        return CLEAR
    half = 1.4 + 2.6 * math.sin(math.pi * min(1.0, L / 16.0))
    off = abs(ang - 0.8) * L
    if off > half:
        return CLEAR
    t = L / 16.0
    c = mix(p["red"], p["orange"], t * 1.6) if t < 0.62 else mix(p["orange"], p["gold"], (t - 0.62) / 0.38)
    if stars(x, y, z, face, cell=1.4, r=0.22, prob=0.25):
        c = p["white"]
    return c, c


def bluewingf(cx, cy, ang, length, width):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = x - cx, y - cy
        c_, s_ = math.cos(ang), math.sin(ang)
        a, b = u * c_ + v * s_, -u * s_ + v * c_
        if a < 0 or a > length or abs(b) > width * math.sin(math.pi * a / length):
            return CLEAR
        if stars(x, y, z, face, cell=1.0, r=0.2, prob=0.3):
            return p["white"] + (230,), p["white"]
        return p["wing_blue"], None
    return s


def build() -> Model:
    m = Model("tangledtime")
    top = m.bone("tangledtime", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 11, 0))
    ellipsoid(m, bd, 0, 11.6, 0.2, 2.2, 2.8, 2.0, bodyf, step=1)                   # small dark green body
    hd = m.bone("head", bd, (0, 14.5, 0))
    ellipsoid(m, hd, 0, 18.4, 0, 4.0, 3.8, 3.4, headf, step=1)                    # big pale head
    for sx, lean in ((1, 0.25), (-1, 0.55)):                                       # red leaf-feather antennae
        rod(m, hd, (sx * 1.6, 21.6, 0.6), (sx * (2.6 + lean * 2), 25.0, 1.6), 1.6, solid("red"), extend=0.4)
        spike(m, hd, (sx * (2.6 + lean * 2), 24.8, 1.6), (sx * lean, 1, 0.2), 1.4, 2.8, solid("red"), tip=0.6)
    spike(m, hd, (2.8, 20.6, -0.6), (0.6, 1, 0.1), 1.2, 3.6, solid("horn"), tip=0.5)          # white horn
    for i in range(4):                                                             # the vine tangle round its head
        rod(m, hd, (3.6, 20.4 - i * 1.2, -1.4 + i * 0.6), (3.8, 19.6 - i * 1.4, 1.0 + i * 0.4), 0.9,
            solid("vine"), extend=0.3)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):
        ar = m.bone(nm, bd, (sx * 1.8, 13.0, -0.4))
        rod(m, ar, (sx * 1.8, 13.0, -0.4), (sx * 3.0, 11.4, -1.6), 1.0, solid("pale"), extend=0.3)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                          # legs and a ragged leaf skirt
        lg = m.bone(nm, bd, (sx * 1.2, 9.4, 0))
        rod(m, lg, (sx * 1.2, 9.6, 0), (sx * 1.6, 5.0, -0.6), 1.6, solid("green_dark"), extend=0.4)
        spike(m, lg, (sx * 1.6, 5.2, -0.6), (sx * 0.3, -1, -0.3), 1.2, 2.4, solid("green_dark"), tip=0.5)
    for i in range(8):
        ang = math.radians(i * 45 + 22.5)
        d = (math.sin(ang), -1.0, math.cos(ang))
        spike(m, bd, (math.sin(ang) * 1.6, 9.6, math.cos(ang) * 1.4), d, 1.4, 3.4, solid("green"), tip=0.6)
    wg = m.bone("wing_left", bd, (2.0, 13.6, 1.6))                                 # the long feather wing
    m.box(wg, 2.0, 13.0, 1.8, 16.0, 30.0, 1.8, featherf)
    wr = m.bone("wing_right", bd, (-2.0, 13.6, 1.6))                               # two small blue wings
    m.box(wr, -9.0, 13.0, 1.8, -1.5, 20.0, 1.8, bluewingf(-2.0, 14.0, math.radians(150), 7.0, 2.0))
    m.box(wr, -9.0, 9.0, 2.0, -1.5, 15.0, 2.0, bluewingf(-2.0, 13.4, math.radians(200), 6.0, 1.6))
    return m
