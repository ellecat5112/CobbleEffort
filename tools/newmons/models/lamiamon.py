"""Lamiamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the serpent lady: a figure with blue hair in two drill twin-tails and a black mask with red eyes and
two small horns, in a frilled crimson-and-blue gown, violet bat wings, carrying a great frilled crimson parasol, her
lower body a long coiled serpent tail in crimson and navy scales ending in a fan fin. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage. Built as officially drawn (fully clothed).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digidetail import cutout, fabric, local, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "a serpent lady with blue drill twin-tails, a black mask, a frilled crimson gown, violet bat wings, a frilled parasol and a long coiled serpent tail"
BASE = {"crimson": (200, 40, 80), "crimson_dark": (120, 14, 40), "navy": (40, 50, 120), "navy_dark": (14, 18, 60),
        "lav": (200, 180, 240), "blue": (70, 110, 220), "blue_dark": (30, 50, 150), "black": (24, 24, 30),
        "eye": (240, 40, 60), "skin": (240, 220, 220), "skin_dark": (190, 160, 160), "violet": (120, 80, 170),
        "violet_dark": (60, 30, 100), "gold": (230, 190, 70)}
SHINY = {"crimson": (60, 160, 120), "crimson_dark": (20, 90, 60), "navy": (200, 160, 60), "navy_dark": (120, 90, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def gownf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if v / max(H, 1e-6) < 0.12:
        return tone(p["lav"], face), None                                            # frilled hem
    return fabric(P, "crimson", "crimson_dark")(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "down") or y < 2.0:
        return scales(P, "navy", "navy_dark", size=1.2)(x, y, z, face, variant, box=box, **k)
    return scales(P, "crimson", "crimson_dark", size=1.4)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("lamiamon")
    top = m.bone("lamiamon", None, (0, 0, 0))
    tb = m.bone("tail", top, (0, 6, 0))                                              # coiled serpent tail
    pts = []
    for i in range(16):
        t = i / 15
        ang = t * 2.2 * math.pi
        r = 9.0 - t * 3.0
        pts.append((r * math.sin(ang), 3.0 + t * 20.0 if i < 12 else 26.0, r * math.cos(ang) + (0 if i < 12 else 0)))
    pts = [(9.0 * math.sin(a), 2.6, 9.0 * math.cos(a) + 2.0) for a in [i * 0.55 for i in range(12)]]
    pts.append((0, 10.0, 0))
    pts.append((0, 22.0, 0))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 3 if j > 2 else 2, tailf, extend=0.8)
    spike(m, tb, pts[0], (1, 0.6, 0.2), 3.0, 6.0, fabric(P, "lav", "violet"), tip=0.8)          # fan fin
    bd = m.bone("body", top, (0, 22, 0))
    for j in range(3):                                                               # frilled gown
        r = 6.0 - j * 1.2
        m.round_box(bd, 0, 0.4, r, r * 0.8, 20.0 + j * 5.0, 26.0 + j * 5.0, gownf, cut=max(1, int(r * 0.3)))
    m.round_box(bd, 0, 0.4, 3.4, 2.8, 34.0, 44.0, fabric(P, "crimson", "crimson_dark"), cut=1)
    m.round_box(bd, 0, -2.6, 1.4, 0.3, 40.0, 42.0, solid(P, "lav"), cut=0)
    hd = m.bone("head", bd, (0, 44, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 44.0, 50.4, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(hd, 0, -2.7, 2.2, 0.3, 46.4, 48.0, solid(P, "black"), cut=0)                  # black mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 46.8, -3.1, max(sx * 0.6, sx * 1.6), 47.4, -3.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.4, 50.0, -1.0), (sx * 0.2, 1, 0.2), 0.9, 2.0, solid(P, "black"), tip=0.8)
        pts = [(sx * 2.4, 49.6, 0.4), (sx * 4.6, 46.0, 1.0), (sx * 5.0, 40.0, 1.0), (sx * 4.6, 34.0, 1.0)]   # drill twin-tails
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 if j < 2 else 1, strands(P, "blue", "blue_dark"), extend=0.4)
    m.round_box(hd, 0, 0.6, 2.8, 2.8, 49.6, 52.0, strands(P, "blue", "blue_dark"), cut=1)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.4, 42.0, 2.6))
        bat_wing(m, wb, (side * 2.4, 42.0, 2.6), 14.0, 12.0, 3, skin(P, "violet", dark="violet_dark"),
                 fabric(P, "violet", "violet_dark"), side=side, sweep=20)
    ab = m.bone("arm_right", bd, (-3.4, 42.0, 0))                                    # frilled parasol
    rod(m, ab, (-3.4, 42.0, 0), (-6.0, 40.0, -2.0), 1, fabric(P, "crimson", "crimson_dark"), extend=0.3, t2=2)
    rod(m, ab, (-6.0, 36.0, -2.0), (-8.0, 58.0, 0), 1, solid(P, "gold"), extend=0, t2=1)
    for j, (r, y0) in enumerate(((9.0, 57.0), (6.0, 59.0), (3.0, 60.6))):
        m.round_box(ab, -8.0, 0, r, r, y0, y0 + 2.0, fabric(P, "crimson", "crimson_dark") if j != 1 else fabric(P, "navy", "navy_dark"),
                    cut=max(1, int(r * 0.4)))
    return m
