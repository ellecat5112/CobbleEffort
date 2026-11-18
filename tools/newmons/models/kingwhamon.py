"""King Whamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the island whale: a vast whale whose head and back are a cliff of grey-brown rock topped with green turf and moss,
a gaping cave of a mouth ringed with white fangs, a pale grey-white tail end with long swept flukes and fins
streaming behind. 35 blocks long.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import fur, local, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 12.0)
KIND = "floater"
K = 2
LOOK = "a vast whale whose head is a cliff of grey-brown rock topped with turf, with a gaping fanged cave mouth and a pale swept tail"
BASE = {"rock": (140, 126, 110), "rock_dark": (80, 70, 60), "rock_light": (190, 180, 166), "grass": (90, 160, 60),
        "grass_dark": (40, 100, 30), "pale": (220, 226, 236), "pale_dark": (150, 160, 180), "mouth": (160, 50, 60),
        "mouth_dark": (80, 20, 30), "tooth": (250, 250, 246), "eye": (30, 30, 34)}
SHINY = {"rock": (110, 120, 160), "rock_dark": (50, 56, 90), "rock_light": (170, 180, 220), "grass": (220, 120, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def rockf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up":
        return fur(P, "grass", "grass_dark")(x, y, z, face, variant, box=box, **k)
    u, v, W, H = local(x, y, z, face, box)
    if (u * 1.7 + math.sin(v * 0.9) * 2.0) % 3.2 < 0.5:
        return tone(p["rock_dark"], face), None
    return tone(p["rock_light"] if v / max(H, 1e-6) > 0.85 else p["rock"], face), None


def build():
    m = Model("kingwhamon")
    top = m.bone("kingwhamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(6):                                                               # cliff head
        z0 = -30.0 + i * 5.0
        h = 34.0 - abs(i - 1.5) * 2.0
        m.round_box(bd, 0, z0 + 2.5, 12.0 - i * 0.4, 2.6, 2.0, h, rockf, cut=2)
    for j, (cx, cz, h) in enumerate(((-6.0, -22.0, 40.0), (4.0, -14.0, 38.0), (-2.0, -26.0, 37.0))):   # crags
        m.round_box(bd, cx, cz, 3.0, 3.0, 30.0, h, rockf, cut=1)
    m.round_box(bd, 0, -31.0, 9.0, 1.2, 6.0, 20.0, solid(P, "mouth_dark"), cut=1)           # cave mouth
    m.round_box(bd, 0, -30.0, 8.4, 1.0, 5.0, 8.0, solid(P, "mouth"), cut=1)
    for j in range(7):
        spike(m, bd, (-7.2 + j * 2.4, 20.0, -31.6), (0, -1, 0), 1.6, 3.6, solid(P, "tooth"), tip=0.8)
        spike(m, bd, (-7.2 + j * 2.4, 6.4, -31.6), (0, 1, 0), 1.4, 2.6, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(bd, min(sx * 11.6, sx * 12.2), 24.0, -22.0, max(sx * 11.6, sx * 12.2), 25.4, -20.0, solid(P, "eye"))
    tb = m.bone("tail", bd, (0, 14, 2))                                              # pale whale tail
    for i in range(7):
        r = 9.0 - i * 1.1
        slab_z(m, tb, 0, 14.0 + i * 0.6, 0.0 + i * 5.0, 5.4 + i * 5.0, r, r * 0.8, skin(P, "pale", dark="pale_dark"))
    for sx in (-1, 1):                                                               # flukes and fins
        spike(m, tb, (sx * 2.0, 18.0, 36.0), (sx * 0.8, 0.4, 0.8), 3.0, 18.0, skin(P, "pale", dark="pale_dark"), tip=0.8)
        spike(m, tb, (sx * 7.0, 10.0, 8.0), (sx, -0.3, 0.8), 2.4, 14.0, skin(P, "pale", dark="pale_dark"), tip=0.8)
    spike(m, tb, (0, 20.0, 14.0), (0, 1, 0.8), 2.0, 8.0, skin(P, "pale", dark="pale_dark"), tip=0.8)
    return m
