"""Ceresmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Olympus goddess of the harvest in her colossal form. A living mountain of earth: a hunched
rock-and-soil giant draped in moss and forest, with a rounded wooded crown for a head, great mossy arms ending in
claws of pale stone, roots and crumbling rocks hanging from its underside, and tiny Ceresmon Medium seated in a
hollow on its chest. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fbm, metal, mix, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = ("a colossal living mountain of earth draped in moss and forest, with a wooded crown for a head, great mossy "
        "arms with pale stone claws and roots trailing beneath")
BASE = {"moss": (90, 130, 50), "moss_dark": (40, 70, 24), "moss_light": (150, 190, 80), "earth": (120, 90, 50),
        "earth_dark": (70, 50, 26), "stone": (220, 210, 170), "stone_dark": (150, 140, 100), "pink": (240, 150, 190),
        "gold": (230, 200, 120), "leaf": (80, 160, 80)}
SHINY = {"moss": (170, 120, 60), "moss_dark": (100, 60, 24), "moss_light": (220, 170, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def mossf(x, y, z, face, variant, box=None, **k):
    """Moss and canopy over earth: noisy greens on top and sides, earth showing through underneath."""
    p = P(variant)
    n = fbm(x * 0.25, y * 0.25, z * 0.25, 5)
    if face == "down" or n < 0.32:
        return tone(mix(p["earth_dark"], p["earth"], n * 2), face), None
    col = p["moss_light"] if n > 0.68 else p["moss"] if n > 0.45 else p["moss_dark"]
    return tone(col, face), None


STONE = metal(P, "stone", dark="stone_dark")


def build():
    m = Model("ceresmon")
    top = m.bone("ceresmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    ball(m, bd, (0, 30.0, 2.0), 16.0, mossf, layers=8, squash=0.75)                   # the mountain body
    for sx in (-1, 1):
        ball(m, bd, (sx * 12.0, 38.0, 0.0), 8.0, mossf, layers=5)                    # shoulders
    hd = m.bone("head", bd, (0, 44, -2))
    ball(m, hd, (0, 50.0, -2.0), 8.6, mossf, layers=6)                               # the wooded crown
    for i in range(10):                                                             # canopy tufts
        ang = math.radians(i * 36)
        ball(m, hd, (6.0 * math.cos(ang), 54.0 + (i % 3), -2.0 + 6.0 * math.sin(ang)), 2.6, mossf, layers=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # great mossy arms
        ab = m.bone(nm, bd, (sx * 14.0, 38.0, 0))
        pts = [(sx * 14.0, 38.0, 0.0), (sx * 22.0, 26.0, -4.0), (sx * 24.0, 12.0, -8.0), (sx * 22.0, 4.0, -12.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, ab, p0, p1, 9 - j * 2, mossf, extend=1.0)
        for j in range(4):
            spike(m, ab, (pts[-1][0] + (j - 1.5) * 1.6, 2.0, pts[-1][2] - 1.0), (0, -0.6, -1), 1.6, 4.0, STONE,
                  tip=0.5)
    for i in range(12):                                                             # roots and crumbling rocks
        ang = math.radians(i * 30)
        rod(m, bd, (8.0 * math.cos(ang), 20.0, 2.0 + 8.0 * math.sin(ang)),
            (13.0 * math.cos(ang), 2.0 + (i % 3), 2.0 + 13.0 * math.sin(ang)), 2, solid(P, "earth"), extend=0.5)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 7.0, 16.0, 2.0))
        m.round_box(lg, sx * 7.0, 2.0, 5.0, 5.0, 0.0, 18.0, mossf, cut=2)
    m.round_box(bd, 0, -12.0, 3.0, 1.2, 33.0, 38.0, solid(P, "earth_dark"), cut=1)  # the chest hollow
    ball(m, bd, (0, 35.6, -13.0), 1.0, solid(P, "pink"), layers=2)                  # tiny Ceresmon Medium
    m.round_box(bd, 0, -13.0, 0.8, 0.8, 33.0, 35.0, solid(P, "leaf"), cut=1)
    return m
