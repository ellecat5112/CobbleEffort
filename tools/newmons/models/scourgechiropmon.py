"""Scourge Chiropmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a stealth-bomber bat: a sleek indigo-and-violet armoured flying machine with swept bat
wings tipped red, a fanged bat-head cockpit with glowing yellow eyes, ribbed violet membrane panels, twin jet
engines burning yellow and a great black bomb slung beneath. 25 blocks.

Front is -z, y is up. 36 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a sleek indigo-and-violet stealth-bomber bat with swept red-tipped wings, a fanged bat-head cockpit, twin jets and a black bomb"
BASE = {"indigo": (70, 70, 150), "indigo_dark": (24, 24, 70), "violet": (140, 70, 200), "violet_dark": (70, 30, 120),
        "red": (210, 40, 40), "black": (30, 30, 36), "black_dark": (10, 10, 12), "eye": (250, 220, 60),
        "jet": (255, 230, 120, 200), "steel": (200, 204, 216), "tooth": (250, 250, 240)}
SHINY = {"indigo": (70, 70, 80), "indigo_dark": (24, 24, 30), "violet": (200, 60, 70), "violet_dark": (120, 20, 30)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "indigo", "indigo_dark", trim="violet", trim_w=0.2)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) > 24.0:
        return tone(p["red"], face), None
    if face in ("up", "down") and abs(x) % 4.0 < 0.4:
        return tone(p["violet_dark"], face), None
    return armour(P, "violet", "violet_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("scourgechiropmon")
    top = m.bone("scourgechiropmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    for i in range(6):                                                                   # fuselage
        t = (i + 0.5) / 6
        r = 4.0 * math.sin(math.pi * (0.2 + 0.7 * t)) + 1.0
        slab_z(m, bd, 0, 20.0, -10.0 + i * 3.6, -10.0 + (i + 1) * 3.6 + 0.2, r * 1.2, r * 0.8, HULL)
    hd = m.bone("head", bd, (0, 21, -10))
    m.round_box(hd, 0, -13.0, 3.0, 3.0, 18.4, 24.0, HULL, cut=1)                            # bat-head cockpit
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 22.0, -16.1, max(sx * 1.0, sx * 2.4), 22.8, -15.9, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 24.0, -12.0), (sx * 0.4, 1, 0.3), 1.4, 5.0, HULL, tip=0.8)    # bat ears
        spike(m, hd, (sx * 1.0, 18.6, -15.6), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):                                                                   # swept bat wings
        for j in range(3):
            x0, x1 = sorted((sx * 4.0, sx * (28.0 - j * 4.0)))
            m.box(bd, x0, 19.4, -4.0 + j * 4.0, x1, 20.6, 0.0 + j * 4.0, wingf,
                  rotation=(0, sx * (20 + j * 8), 0), pivot=(sx * 4.0, 20.0, -2.0 + j * 4.0))
        rod(m, bd, (sx * 6.0, 18.0, 2.0), (sx * 6.0, 18.0, 12.0), 3, metal(P, "steel"), extend=0.4)   # jets
        spike(m, bd, (sx * 6.0, 18.0, 12.4), (0, 0, 1), 2.0, 5.0, solid(P, "jet", glow=True), tip=0.8)
    rod(m, bd, (0, 12.0, -6.0), (0, 12.0, 10.0), 5, metal(P, "black", dark="black_dark"), extend=0.4)   # bomb
    spike(m, bd, (0, 12.0, -6.4), (0, 0, -1), 2.4, 3.0, metal(P, "black", dark="black_dark"), tip=0.8)
    for sx in (-1, 1):
        m.box(bd, min(sx * 0.3, sx * 3.0), 11.0, 9.0, max(sx * 0.3, sx * 3.0), 13.0, 12.0, metal(P, "black"))
    return m
