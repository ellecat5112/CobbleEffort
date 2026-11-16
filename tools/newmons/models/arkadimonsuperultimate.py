"""Arkadimon Super Ultimate (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): the final form of the bewitching beast, an armoured head-body of dark steel plates
the size of a hill. One great amber eye under a hooked crest, folded steel plates like a closed carapace, a mane of
black hair spilling round it and long black whip-antennae trailing out. 45 blocks tall.

Front is -z, y is up. 52 units tall; Super Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _arkadi import P, STEEL
from _digidetail import eye, fur, plane, solid, strands
from _route import tone

HEIGHT = 52
SCALE, HITBOX = sized(45, HEIGHT, 3.4)
KIND = "floater"
K = 3
LOOK = ("an armoured head-body of dark steel plates with one great amber eye under a hooked crest, a mane of black "
        "hair and long black whip-antennae")
HAIR = strands(P, "hair", "hair", tip="hair_light")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        c = eye(p, a + 6.0, b - 32.0, 2.4, "eye", slit=True)
        if c is not None:
            return c, (p["eye"] if c == p["eye"] else None)
    return STEEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("arkadimonsuperultimate")
    top = m.bone("arkadimonsuperultimate", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    ball(m, bd, (0, 26.0, 0), 15.0, headf, layers=9, squash=0.9)
    for sx in (-1, 1):                                           # folded carapace plates
        for j in range(3):
            m.box(bd, min(sx * 6.0, sx * 17.0), 30.0 - j * 7.0, -10.0 + j * 2.0, max(sx * 6.0, sx * 17.0),
                  36.0 - j * 7.0, 6.0 + j * 2.0, STEEL, rotation=(0, 0, sx * (20 - j * 10)), pivot=(sx * 6.0, 33.0, 0))
    rod(m, bd, (0, 40.0, -6.0), (0, 46.0, -10.0), 4, STEEL, extend=0.4)                  # hooked crest
    spike(m, bd, (0, 46.0, -10.0), (0, -0.6, -1), 3.0, 4.0, STEEL)
    hr = m.bone("mane", bd, (0, 20, 4))
    for i in range(20):                                          # black hair spilling round its lower half
        ang = math.radians(i * 18)
        base = (13.0 * math.sin(ang), 16.0, 12.0 * math.cos(ang))
        tip = (17.0 * math.sin(ang), 2.0 + (i % 3) * 2, 16.0 * math.cos(ang))
        rod(m, hr, base, tip, 4, HAIR, extend=0.5, t2=3)
    for sx in (-1, 1):                                           # whip antennae
        ab = m.bone("ant_left" if sx > 0 else "ant_right", bd, (sx * 4.0, 40.0, 0))
        pts = [(sx * 4.0, 40.0, 0.0), (sx * 10.0, 50.0, 2.0), (sx * 20.0, 52.0, 4.0), (sx * 30.0, 46.0, 6.0),
               (sx * 36.0, 38.0, 8.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, solid(P, "hair"), extend=0.3)
    return m
