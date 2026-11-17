"""Calamaramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Hybrid of the deep sea. A great white squid with a violet-finned arrowhead mantle, two huge
yellow eyes, black hooked fins and long pale-blue tentacles looping round it, studded with spikes and ending in
clawed hooks; a small armoured rider in a pointed squid-hood helm and a pale bodysuit sits atop the head, hands
raised. 25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, eye, local, mix, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a great white squid with a violet-finned arrowhead mantle, huge yellow eyes and spiked pale-blue tentacles, "
        "ridden by a small armoured figure in a pointed squid-hood helm")
BASE = {"white": (240, 242, 250), "white_dark": (176, 180, 200), "violet": (170, 120, 200), "violet_dark": (100, 60, 140),
        "tent": (150, 180, 230), "tent_dark": (80, 110, 180), "tent_light": (210, 226, 250), "spike": (230, 232, 240),
        "black": (30, 30, 40), "eye": (250, 210, 40), "pupil": (40, 20, 10), "red": (200, 40, 50),
        "suit": (230, 226, 240), "suit_dark": (170, 166, 190), "hair": (190, 160, 210), "skin": (240, 214, 200)}
SHINY = {"white": (60, 60, 80), "white_dark": (26, 26, 40), "tent": (230, 110, 140), "tent_dark": (160, 50, 80),
         "tent_light": (255, 190, 210), "violet": (60, 180, 170), "violet_dark": (20, 110, 100)}


def P(v):
    return pal(BASE, SHINY, v)


MANTLE = armour(P, "white", "white_dark", trim="violet", trim_w=0.4)
TENT = skin(P, "tent", dark="tent_dark", light="tent_light", var=0.04)
SUIT = armour(P, "suit", "suit_dark")


def headf(x, y, z, face, variant, box=None, **k):
    """The squid's head: two huge yellow eyes on the front."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 3.6, y - 30.0, 2.6, "eye", slit=True)
            if c is not None:
                return c, None
    return MANTLE(x, y, z, face, variant, box=box, **k)


def finf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["violet_dark"] if (u * 1.2) % 2.0 < 0.3 else p["violet"], face), None


def build():
    m = Model("calamaramon")
    top = m.bone("calamaramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    # the arrowhead mantle: slices tapering up and back to a point
    for i in range(8):
        y0 = 30.0 + i * 3.0
        r = 7.0 * (1 - i / 9) + 1.0
        m.round_box(bd, 0, 2.0 + i * 1.6, r, r * 0.8, y0, y0 + 3.4, MANTLE, cut=max(1, round(r * 0.3)))
    spike(m, bd, (0, 54.0, 15.0), (0, 1, 0.8), 2.4, 4.0, MANTLE)
    for sx in (-1, 1):                                                  # violet side fins
        x0, x1 = sorted((sx * 4.0, sx * 15.0))
        m.box(bd, x0, 38.0, 6.0, x1, 52.0, 6.0, finf, rotation=(-30, sx * 30, -sx * 20), pivot=(sx * 4.0, 45.0, 6.0))
        spike(m, bd, (sx * 6.0, 33.0, 2.0), (sx, 0.2, 0.6), 1.6, 6.0, solid(P, "black"), tip=0.6)
    hd = m.bone("head", bd, (0, 28, 0))
    m.round_box(hd, 0, 0.0, 7.4, 6.4, 22.0, 34.0, headf, cut=2)          # the head with the eyes
    # tentacles: eight looping arms with spikes and hooked tips
    for k in range(8):
        ang = math.radians(k * 45 + 22.5)
        tb = m.bone(f"tentacle_{k}", hd, (0, 22, 0))
        loop = 1.0 if k in (1, 6) else 0.0
        pts = [(4.0 * math.cos(ang), 22.0, 4.0 * math.sin(ang))]
        for j in range(1, 7):
            rr = 4.0 + j * 2.6 + loop * 6.0 * math.sin(j * 0.6)
            yy = 22.0 - j * 3.6 + loop * 10.0 * math.sin(j * 0.5)
            a2 = ang + 0.12 * j * (1 if k % 2 else -1)
            pts.append((rr * math.cos(a2), max(1.0, yy), rr * math.sin(a2)))
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tb, p0, p1, max(1, 3 - j // 2), TENT, extend=0.6)
            if j % 2:
                spike(m, tb, p1, (math.cos(ang), 0.6, math.sin(ang)), 0.8, 1.6, solid(P, "spike"))
        spike(m, tb, pts[-1], (math.cos(ang), -0.4, math.sin(ang)), 1.2, 2.6, solid(P, "spike"), tip=0.4)
    # the rider on top of the head
    rd = m.bone("rider", hd, (0, 34, -1))
    m.round_box(rd, 0, -1.0, 1.6, 1.2, 34.0, 38.6, SUIT, cut=1)                     # torso
    m.round_box(rd, 0, -1.0, 1.2, 1.2, 38.6, 41.0, solid(P, "skin"), cut=1)          # face
    spike(m, rd, (0, 40.6, -1.0), (0, 1, 0.3), 3.0, 4.2, SUIT, tip=0.6)              # squid-hood helm
    for sx in (-1, 1):
        rod(m, rd, (sx * 1.6, 37.6, -1.0), (sx * 4.6, 40.0, -2.4), 1, SUIT, extend=0.3)
        for j in range(3):
            spike(m, rd, (sx * 4.8, 40.0, -2.4), (sx * 0.4, 1, -0.2 + j * 0.2), 0.6, 1.4, solid(P, "red"))
        rod(m, rd, (sx * 0.8, 34.0, -1.0), (sx * 2.0, 33.6, -4.0), 1, SUIT, extend=0.3)
        rod(m, rd, (sx * 1.0, 40.0, -0.2), (sx * 2.4, 36.0, 1.0), 1, solid(P, "hair"), extend=0.2, t2=2)
    return m
