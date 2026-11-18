"""Metal Seadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a sea serpent plated in gold Chrondigizoit: a long coiled body of gold armour plates
with silver-grey seams, a dragon's head in a gold helmet with a long nose cannon and swept horns, a shaggy grey mane
streaming back, rows of steel blade-fins along its back and a long silver tail ending in a gold blade. 35 blocks long.

Front is -z, y is up. 48 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a sea serpent plated in gold armour with a helmeted dragon head and nose cannon, a shaggy grey mane, steel "
        "blade-fins along its back and a silver tail ending in a gold blade")
BASE = {"gold": (230, 200, 90), "gold_dark": (150, 120, 30), "gold_light": (255, 240, 170), "steel": (200, 204, 214),
        "steel_dark": (100, 104, 116), "mane": (150, 150, 160), "mane_dark": (80, 80, 90), "eye": (250, 60, 60),
        "mouth": (170, 30, 50), "tooth": (250, 250, 240)}
SHINY = {"gold": (130, 160, 230), "gold_dark": (60, 80, 150), "gold_light": (210, 225, 255), "mane": (230, 220, 200)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="steel_dark", trim_w=0.25, rivets=True)
STEEL = metal(P, "steel", dark="steel_dark")
MANE = strands(P, "mane", "mane_dark")


def build():
    m = Model("metalseadramon")
    top = m.bone("metalseadramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    pts = []
    for i in range(28):                                                                  # coiled body
        t = i / 27
        ang = t * 3.4 * math.pi
        r = 10.0 - 3.0 * t
        pts.append((r * math.cos(ang + 1.2) * 0.9, 34.0 - 30.0 * t + 3.0 * math.sin(ang), r * math.sin(ang + 1.2)))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        r = 6 if j < 8 else 5 if j < 15 else 4 if j < 20 else 3
        rod(m, bd, p0, p1, r, GOLD if j < 21 else STEEL, extend=0.7)
        if j % 3 == 1 and j < 21:
            spike(m, bd, p0, (0, 1, 0.4), 1.4, 5.0, STEEL, tip=0.8)                         # back blade-fins
    e = pts[-1]
    spike(m, bd, e, (-0.5, -0.2, -1), 2.4, 8.0, GOLD, tip=0.8)                             # gold tail blade
    h = pts[0]
    hd = m.bone("head", bd, h)
    hx, hy, hz = h[0], h[1] + 4.0, h[2] - 3.0
    m.round_box(hd, hx, hz - 3.0, 5.0, 6.0, hy - 3.0, hy + 4.0, GOLD, cut=1)                 # gold helmet
    m.round_box(hd, hx, hz - 11.0, 3.6, 5.0, hy - 1.0, hy + 2.6, GOLD, cut=1)                # upper jaw
    m.round_box(hd, hx, hz - 10.0, 3.0, 4.6, hy - 3.6, hy - 1.6, GOLD, cut=1)                # lower jaw
    m.box(hd, hx - 2.6, hy - 1.6, hz - 14.0, hx + 2.6, hy - 1.0, hz - 6.0, solid(P, "mouth"))
    for j in range(5):
        for sx in (-1, 1):
            spike(m, hd, (hx + sx * 2.8, hy - 1.0, hz - 14.0 + j * 1.6), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
    rod(m, hd, (hx, hy + 2.6, hz - 10.0), (hx, hy + 3.4, hz - 18.0), 2, STEEL, extend=0.3)  # nose cannon
    for sx in (-1, 1):
        m.box(hd, hx + min(sx * 5.0, sx * 5.2), hy + 1.6, hz - 6.0, hx + max(sx * 5.0, sx * 5.2), hy + 2.8, hz - 4.0,
              solid(P, "eye", glow=True))
        spike(m, hd, (hx + sx * 3.4, hy + 4.0, hz - 1.0), (sx * 0.4, 0.7, 1), 1.6, 8.0, GOLD, tip=0.8)   # swept horns
    for row in range(3):                                                                 # shaggy grey mane
        for i in range(5):
            ang = math.radians(-50 + i * 25)
            spike(m, hd, (hx + 4.0 * math.sin(ang), hy + 3.0 - row * 2.4, hz + 2.0 + row),
                  (math.sin(ang) * 0.6, 0.3 - row * 0.3, 1), 2.0, 12.0 - row * 2.0, MANE, tip=0.8)
    return m
