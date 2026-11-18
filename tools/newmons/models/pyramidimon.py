"""Pyramidimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a living pyramid of golden sandstone bricks, point down, wreathed in a storm of churning sand
that boils up over it into a cloud with a dim stony face and a golden scarab ornament; little pyramids orbit it, and
from the sand reach two great jointed brown-stone arms with golden cuffs and red-and-gold crane claws. 35 blocks.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, noise2, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a living golden sandstone pyramid point down, wreathed in a churning sand cloud, with jointed stone arms and red-and-gold claws"
BASE = {"gold": (240, 200, 90), "gold_dark": (170, 130, 40), "mortar": (150, 110, 40), "sand": (190, 170, 110),
        "sand_dark": (120, 100, 60), "stone": (110, 80, 60), "stone_dark": (60, 40, 30), "red": (200, 40, 40),
        "red_dark": (120, 14, 14), "eye": (250, 80, 40), "steel": (220, 190, 100)}
SHINY = {"gold": (220, 224, 236), "gold_dark": (140, 144, 160), "sand": (140, 140, 160), "sand_dark": (80, 80, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def brickf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    row = math.floor(y / 1.6)
    u = (x + z) + (row % 2) * 1.4
    if (y % 1.6) < 0.2 or (u % 2.8) < 0.2:
        return tone(p["mortar"], face), None
    return tone(p["gold"] if face != "down" else p["gold_dark"], face), None


def sandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    n = noise2(x * 0.4 + z * 0.3, y * 0.4, 5)
    c = p["sand"] if n < 0.55 else p["sand_dark"]
    if face == "north" and 38.0 < y < 44.0:
        for sx in (-1, 1):
            if math.hypot(x - sx * 3.0, y - 41.0) < 1.0:
                return p["eye"], p["eye"]
    return tone(c, face), None


STONE = armour(P, "stone", "stone_dark", panel=(3.0, 3.0))
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("pyramidimon")
    top = m.bone("pyramidimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    for i in range(10):                                                                  # inverted pyramid
        w = 1.0 + i * 1.6
        m.box(bd, -w, 4.0 + i * 2.6, -w, w, 6.6 + i * 2.6, w, brickf)
    for c, r in (((0, 38.0, 4.0), 12.0), ((-10.0, 36.0, 6.0), 8.0), ((10.0, 36.0, 6.0), 8.0), ((0, 46.0, 6.0), 9.0),
                 ((-6.0, 44.0, 10.0), 7.0), ((7.0, 44.0, 10.0), 7.0)):                     # churning sand cloud
        ball(m, bd, c, r, sandf, layers=5, ry=r * 0.75)
    m.round_box(bd, 0, -8.0, 1.6, 0.6, 46.0, 50.0, GOLD, cut=0)                            # golden scarab ornament
    spike(m, bd, (0, 50.0, -8.0), (0, 1, 0), 1.6, 3.0, GOLD, tip=0.8)
    orb = m.bone("ring_pyramids", bd, (0, 34, 0))                                         # orbiting pyramids
    for j, (ang, h) in enumerate(((30, 50.0), (150, 44.0), (260, 30.0))):
        a = math.radians(ang)
        cx, cz = 22.0 * math.cos(a), 22.0 * math.sin(a)
        for i in range(3):
            w = 3.0 - i
            m.box(orb, cx - w, h + i * 1.6, cz - w, cx + w, h + (i + 1) * 1.6, cz + w, brickf)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                   # stone arms + crane claws
        ab = m.bone(nm, bd, (sx * 14.0, 34.0, 0))
        el = (sx * 24.0, 30.0, -4.0)
        wr = (sx * 28.0, 18.0, -6.0)
        rod(m, ab, (sx * 14.0, 34.0, 0), el, 5, STONE, extend=0.8)
        rod(m, ab, el, wr, 4, STONE, extend=0.8)
        m.round_box(ab, wr[0], wr[2], 3.6, 3.6, wr[1], wr[1] + 3.0, GOLD, cut=1)
        for f in range(4):
            ang = 2 * math.pi * f / 4
            d = (0.5 * math.cos(ang), -1, 0.5 * math.sin(ang))
            spike(m, ab, (wr[0] + 2.4 * math.cos(ang), wr[1], wr[2] + 2.4 * math.sin(ang)), d, 1.6, 9.0,
                  armour(P, "red", "red_dark", trim="gold", trim_w=0.3), tip=0.8)
    return m
