"""Big Ukkomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): an
ancient fairy spirit like a great pink curled grub-ghost. A soft pink body bent into a crescent, two small pointed
fins, a gaping toothy mouth under round pale eyes, a violet orb glowing in its belly, a long tail curling over its
head, wrapped in drifting lilac clouds. 35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import gem, plane, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("an ancient fairy spirit: a soft pink crescent body with small fins, a toothy mouth, round pale eyes, a "
        "glowing violet orb and a long curling tail in drifting lilac clouds")
BASE = {"pink": (240, 200, 210), "pink_dark": (200, 140, 160), "pink_light": (255, 236, 240), "violet": (150, 110, 230),
        "violet_light": (230, 210, 255), "cloud": (220, 210, 240, 190), "black": (40, 30, 40), "tooth": (250, 250, 246),
        "eye": (250, 220, 230)}
SHINY = {"pink": (200, 230, 240), "pink_dark": (140, 180, 200), "pink_light": (240, 250, 255),
         "violet": (240, 180, 60), "violet_light": (255, 240, 180)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "pink", dark="pink_dark", light="pink_light", var=0.03)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 3.6, b - 40.0) < 1.6:
                return tone(p["pink_light"], face), None
        if abs(a) < 4.0 and 33.4 < b < 36.0:
            jag = abs(((a * 1.4) % 2) - 1) * 0.8
            return (p["tooth"] if (b > 36.0 - jag or b < 33.4 + jag) else p["black"]), None
    return BODY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bigukkomon")
    top = m.bone("bigukkomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    pts = []
    for i in range(10):                                          # the crescent body: head high, belly low
        t = i / 9
        ang = math.radians(140 - 160 * t)
        pts.append((12.0 * math.cos(ang) * 0.7, 26.0 + 14.0 * math.sin(ang), -2.0))
    for i, p in enumerate(pts):
        r = 7.0 - abs(i - 2) * 0.55
        ball(m, bd, p, max(2.0, r), headf if i == 1 else BODY, layers=4)
    ball(m, bd, (pts[4][0], pts[4][1], -7.0), 2.4, gem(P, "violet", "violet_light"), layers=3)
    for sx in (-1, 1):                                           # small fins
        spike(m, bd, (pts[1][0] + sx * 5.0, pts[1][1] + 4.0, -1.0), (sx, 0.6, 0.2), 2.4, 4.0, BODY, tip=0.8)
    tl = m.bone("tail", bd, pts[-1])
    q = pts[-1]
    for j in range(6):                                           # tail curling up over the head
        ang = math.radians(-40 + j * 32)
        n = (q[0] + 4.0 * math.cos(ang), q[1] + 4.0 * math.sin(ang) + 2.0, q[2])
        rod(m, tl, q, n, max(1, round(5 - j * 0.8)), BODY, extend=0.5)
        q = n
    cl = m.bone("cap", bd, (0, 14, 0))
    for j in range(8):                                           # drifting clouds
        ang = math.radians(j * 45)
        ball(m, cl, (14.0 * math.cos(ang), 14.0 + (j % 3) * 4.0, 10.0 * math.sin(ang)), 4.0, solid(P, "cloud"),
             layers=3)
    return m
