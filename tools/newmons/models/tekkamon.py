"""Tekkamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a floating violet iron ball with a stitched seam and a wide grinning mouth of teeth, two jointed
mechanical arms ending in big brown hands, one gripping a long gleaming katana with a gold guard, and an arc of
golden energy swept behind the blade. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a floating violet iron ball with a stitched seam and a toothy grin, jointed arms with brown hands and a long katana"
BASE = {"violet": (130, 110, 170), "violet_dark": (60, 50, 90), "seam": (40, 30, 60), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 126), "brown": (130, 80, 50), "brown_dark": (70, 40, 20), "gold": (230, 180, 60),
        "tooth": (250, 250, 244), "mouth": (40, 10, 20), "eye": (250, 60, 60), "arc": (255, 220, 90, 170),
        "joint": (90, 90, 110)}
SHINY = {"violet": (200, 120, 60), "violet_dark": (120, 60, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def ballf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) < 0.35 and z > -6.0:
        return tone(p["seam"], face), None
    if face == "north":
        a, b = plane(x, y, z, face)
        if 16.0 < b < 19.0 and abs(a) < 4.6 - (19.0 - b) * 0.4:
            if abs(b - 17.5) < 0.25:
                return p["mouth"], None
            return (p["tooth"] if (a * 1.4) % 1.0 > 0.18 else p["mouth"]), None
        for sx in (-1, 1):
            if math.hypot(a - sx * 2.4, b - 22.0) < 0.9:
                return p["eye"], p["eye"]
    return metal(P, "violet", dark="violet_dark")(x, y, z, face, variant, box=box, **k)


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["steel"] if y > (box.lo[1] + box.size[1] * 0.4 if box else 0) else p["steel_dark"], face), None


def build():
    m = Model("tekkamon")
    top = m.bone("tekkamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 20.0, 0), 7.0, ballf, layers=6)
    J = solid(P, "joint")
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 18.0, 0))
        pts = [(sx * 6.0, 18.0, 0), (sx * 10.0, 22.0, -2.0), (sx * 13.0, 26.0 if sx > 0 else 12.0, -4.0)]
        for p0, p1 in zip(pts, pts[1:]):
            for t in range(5):
                c = [p0[i] + (p1[i] - p0[i]) * t / 4 for i in range(3)]
                ball(m, ab, tuple(c), 0.9, J, layers=1)
        h = pts[-1]
        m.round_box(ab, h[0], h[2] - 1.0, 2.0, 2.2, h[1] - 2.0, h[1] + 2.4, skin(P, "brown", dark="brown_dark"), cut=1)
        for f in range(4):
            m.box(ab, h[0] - 1.8 + f * 1.0, h[1] + 2.4, h[2] - 3.0, h[0] - 1.0 + f * 1.0, h[1] + 4.4, h[2] - 2.0,
                  skin(P, "brown", dark="brown_dark"))
        if sx < 0:                                                                   # the katana, held level
            m.box(ab, h[0] - 0.5, h[1] - 0.6, h[2] - 1.6, h[0] + 0.5, h[1] + 0.6, h[2] + 3.0, solid(P, "brown_dark"))
            m.box(ab, h[0] - 1.6, h[1] - 1.6, h[2] - 2.4, h[0] + 1.6, h[1] + 1.6, h[2] - 1.6, metal(P, "gold"))
            m.box(ab, h[0] - 0.4, h[1] - 0.9, h[2] - 26.0, h[0] + 0.4, h[1] + 0.9, h[2] - 2.4, bladef,
                  rotation=(0, 40, 0), pivot=(h[0], h[1], h[2] - 2.0))
    arc = m.bone("arc", bd, (0, 14, 0))                                               # golden energy sweep
    for i in range(12):
        ang = math.pi * (0.1 + i / 14)
        cx, cz = -14.0 * math.cos(ang) - 4.0, -14.0 * math.sin(ang)
        m.box(arc, cx - 1.4, 11.0, cz - 1.4, cx + 1.4, 13.6, cz + 1.4, solid(P, "arc", glow=True))
    return m
