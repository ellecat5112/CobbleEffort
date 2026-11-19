"""Scud Missimon (a Digimon of the CobbleEffort: Digital crossover; built after the manga panel on wikimon.net, its
only picture): a monstrous launch rig: a great triangular stippled-grey warhead of a head with one spiralling eye and
jagged fang plates, a cluster of mushroom-capped launch tubes bristling from its crown, and heavy segmented white
armour rolling out behind it like a missile carrier. 15 blocks. Adult stage (no level on wikimon; by analogy with
Missimon's line).

Front is -z, y is up. 40 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a monstrous launch rig: a triangular grey warhead head with one spiral eye and fang plates, mushroom-capped launch tubes and white armour"
BASE = {"grey": (150, 150, 158), "grey_dark": (80, 80, 88), "white": (236, 236, 240), "white_dark": (170, 172, 184),
        "black": (24, 24, 28), "cap": (40, 40, 44), "spot": (240, 240, 240), "eye": (250, 250, 250)}
SHINY = {"grey": (170, 90, 60), "grey_dark": (100, 40, 20), "white": (240, 220, 160), "white_dark": (190, 160, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 24.0)
        if d < 3.0:
            return tone(p["black"] if (d + math.atan2(y - 24.0, x) * 0.3) % 1.0 < 0.4 else p["eye"], face), None
    if (int(x * 2) + int(y * 2) + int(z * 2)) % 3 == 0:
        return tone(p["grey_dark"], face), None
    return tone(p["grey"], face), None


def capf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up" and math.sin(x * 2.0) * math.sin(z * 2.0) > 0.5:
        return tone(p["spot"], face), None
    return tone(p["cap"], face), None


def build():
    m = Model("scudmissimon")
    top = m.bone("scudmissimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(5):                                                                   # rolling armour segments
        slab_z(m, bd, 0, 12.0, 2.0 + i * 5.0, 6.6 + i * 5.0, 9.0 - i * 0.6, 7.0 - i * 0.4,
               armour(P, "white", "white_dark", trim="grey_dark", trim_w=0.3))
    for sx in (-1, 1):
        rod(m, bd, (sx * 10.0, 8.0, 4.0), (sx * 10.0, 8.0, 22.0), 6, armour(P, "white", "white_dark"), extend=0.4)
    hd = m.bone("head", bd, (0, 22, -4))
    for i in range(6):                                                                   # triangular warhead head
        w = 12.0 - i * 2.0
        m.box(hd, -w / 2, 14.0 + i * 3.4, -10.0, w / 2, 17.4 + i * 3.4, 2.0, headf)
    for j in range(5):                                                                   # jagged fang plates
        spike(m, hd, (-6.0 + j * 3.0, 14.4, -10.0), (0, -1, -0.4), 1.2, 3.0, solid(P, "white"), tip=0.8)
    for j in range(6):                                                                   # mushroom launch tubes
        ang = math.radians(-60 + j * 24)
        base_ = (6.0 * math.sin(ang), 30.0 + j % 2, -2.0 + 2.0 * math.cos(ang))
        tip_ = (base_[0] * 1.6, 38.0 + (j % 3), base_[2] + 2.0)
        rod(m, hd, base_, tip_, 2, solid(P, "white"), extend=0.2)
        ball(m, hd, tip_, 2.0, capf, layers=2, squash=1.0, ry=1.2)
    return m
