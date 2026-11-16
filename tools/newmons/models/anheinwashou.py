"""AnheiNüwashou (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net, which shows
only a silhouette): a dark goddess known so far only as a shadow. A tall dusky form with a serpent's coiled lower
body, broad hooded shoulders, two looping horn-crests rising from its head and long arms, wreathed in a faint violet
glow. Built as the silhouette itself: smoky charcoal with a few glowing violet traces. 35 blocks tall.

Front is -z, y is up. 70 units tall; no level known (Ultimate used: a goddess of the Nüwa myth).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fbm, local, mix, plane
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "floater"
K = 3
LOOK = ("a dark goddess known only as a shadow: a serpent-coiled form with hooded shoulders, looping horn-crests and "
        "long arms, smoky charcoal with faint glowing violet traces")
BASE = {"smoke": (64, 60, 66), "smoke_dark": (30, 28, 32), "glow": (170, 110, 240)}
SHINY = {"smoke": (210, 206, 214), "smoke_dark": (150, 146, 160), "glow": (240, 200, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def smokef(x, y, z, face, variant, box=None, **k):
    """Smoky shadow: soft cloudy mottling and thin glowing violet veins."""
    p = P(variant)
    n = fbm(x * 0.25, y * 0.25, z * 0.25, 7)
    a, b = plane(x, y, z, face)
    if abs(math.sin(a * 0.7 + math.sin(b * 0.3) * 3) - 0.0) < 0.03 and (b % 9) < 3:
        return p["glow"], p["glow"]
    return tone(mix(p["smoke_dark"], p["smoke"], 0.3 + 0.7 * n), face), None


def build():
    m = Model("anheinwashou")
    top = m.bone("anheinwashou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    tl = m.bone("tail", bd, (0, 22, 0))
    for i in range(16):                                          # the serpent coil under the body
        ang = i * 0.55
        r = 9.0 - i * 0.25
        c = (r * math.cos(ang), 2.0 + i * 1.1, r * math.sin(ang) * 0.8)
        nx = ((r - 0.25) * math.cos(ang + 0.55), 3.1 + i * 1.1, (r - 0.25) * math.sin(ang + 0.55) * 0.8)
        rod(m, tl, c, nx, 6 - i // 5, smokef, extend=0.8)
    for i in range(6):                                           # torso rising out of the coil
        r = 5.6 + (i - 2.5) * 0.3 if i > 2 else 4.6 + i * 0.3
        m.round_box(bd, 0, 0, r, r * 0.7, 20.0 + i * 5.0, 25.4 + i * 5.0, smokef, cut=2)
    for sx in (-1, 1):                                           # hooded shoulders sweeping out
        rod(m, bd, (0, 48.0, 0), (sx * 12.0, 46.0, 1.0), 5, smokef, extend=0.6, t2=4)
        spike(m, bd, (sx * 12.0, 46.0, 1.0), (sx * 1, -0.5, 0), 3.0, 4.0, smokef, tip=1.4)
    hd = m.bone("head", bd, (0, 52, 0))
    ball(m, hd, (0, 55.0, 0), 4.4, smokef, layers=5)
    for sx in (-1, 1):                                           # two looping horn-crests
        pts = [(sx * 2.4, 58.0, 0), (sx * 6.0, 64.0, 0.6), (sx * 11.0, 66.0, 1.0), (sx * 13.0, 62.0, 1.0),
               (sx * 10.0, 59.0, 1.0), (sx * 7.0, 62.0, 0.8)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, smokef, extend=0.4)
        rod(m, hd, (sx * 1.0, 59.0, 0), (sx * 2.0, 69.0, 0.4), 1, smokef, extend=0.3)  # antenna loops
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):           # long arms hanging out wide
        ab = m.bone(nm, bd, (sx * 11.0, 45.0, 1.0))
        pts = [(sx * 11.0, 45.0, 1.0), (sx * 15.0, 32.0, 0.0), (sx * 17.0, 20.0, -2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 3, smokef, extend=0.6)
        for f in range(4):
            spike(m, ab, pts[-1], (sx * 0.3 + (f - 1.5) * 0.15, -1, -0.2), 1.0, 3.6, smokef)
    return m
