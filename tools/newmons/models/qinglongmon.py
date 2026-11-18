"""Qinglongmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the azure dragon of the east, one of the Four Holy Beasts: a long serpentine body of pale
blue-white cloud-scales bound in coiling iron chains, a crown of white feathered wings along its back, twelve violet
orbs set along its flanks, a dark navy horned head streaked with yellow lightning and trailing a long white mane and
beard, and a tail that crackles away into lightning. 35 blocks.

Front is -z, y is up. 52 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import armour, feathers, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 52
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a long serpentine azure dragon bound in iron chains with white feathered wings, violet orbs and a navy lightning-streaked head"
BASE = {"cloud": (200, 220, 246), "cloud_dark": (110, 150, 210), "navy": (40, 50, 110), "navy_dark": (14, 18, 50),
        "bolt": (250, 220, 60), "white": (248, 248, 252), "white_dark": (190, 196, 214), "chain": (110, 110, 120),
        "chain_dark": (50, 50, 56), "orb": (170, 150, 230), "orb_light": (240, 230, 255), "eye": (250, 220, 60)}
SHINY = {"cloud": (230, 210, 250), "cloud_dark": (160, 120, 220), "navy": (110, 30, 120), "navy_dark": (50, 10, 60)}


def P(v):
    return pal(BASE, SHINY, v)


CLOUD = scales(P, "cloud", "cloud_dark", size=2.0)
CHAIN = metal(P, "chain", dark="chain_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "east", "west") and abs(math.sin(z * 1.1 + y * 0.8) - 0.5 * math.cos(x * 0.9)) < 0.12:
        return tone(p["bolt"], face), p["bolt"]
    return armour(P, "navy", "navy_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("qinglongmon")
    top = m.bone("qinglongmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    pts = [(0, 30.0, -16.0)]
    for i in range(1, 11):                                                               # serpentine coil
        t = i / 10
        pts.append((10.0 * math.sin(t * math.pi * 2.0), 30.0 + 8.0 * math.sin(t * math.pi * 3.0) - t * 14.0,
                    -16.0 + t * 46.0))
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        r = 8 - i // 2
        b = m.bone(f"coil_{i}", bd, p0)
        rod(m, b, p0, p1, max(3, r), CLOUD, extend=1.0)
        for c in range(2):                                                               # wrapping chains
            q = (p0[0] + (p1[0] - p0[0]) * (0.3 + c * 0.4), p0[1] + (p1[1] - p0[1]) * (0.3 + c * 0.4),
                 p0[2] + (p1[2] - p0[2]) * (0.3 + c * 0.4))
            m.round_box(b, q[0], q[2], r * 0.6 + 0.6, r * 0.6 + 0.6, q[1] - 0.5, q[1] + 0.5, CHAIN, cut=1)
        if i % 2 == 0 and i < 8:                                                         # violet orbs
            for sx in (-1, 1):
                ball(m, b, (p0[0] + sx * (r * 0.5 + 1.0), p0[1] - 2.0, p0[2]), 1.2, solid(P, "orb", glow=True), layers=1)
        if 1 <= i <= 6:                                                                  # white feathered wings
            spike(m, b, (p0[0], p0[1] + r * 0.5, p0[2]), (0, 1, 0.4), 2.4, 8.0 + (i % 3) * 3.0,
                  feathers(P, "white", "white_dark"), tip=0.8)
    for sx in (-1, 1):
        feather_wing(m, "coil_2", (pts[2][0] + sx * 3.0, pts[2][1] + 3.0, pts[2][2]), 18.0, 10.0, 5,
                     feathers(P, "white", "white_dark"), side=sx, sweep=30, droop=-10.0)
    tb = m.bone("tail_bolt", "coil_9", pts[-1])
    q = pts[-1]
    for j in range(4):                                                                   # tail crackling to lightning
        q2 = (q[0] + (2.0 if j % 2 else -2.0), q[1] + 1.6, q[2] + 3.0)
        rod(m, tb, q, q2, 1, solid(P, "bolt", glow=True), extend=0.2)
        q = q2
    hd = m.bone("head", bd, pts[0])
    m.round_box(hd, 0, -22.0, 4.0, 6.0, 27.0, 34.0, headf, cut=2)                         # navy head
    m.round_box(hd, 0, -30.0, 2.6, 3.0, 27.0, 31.0, headf, cut=1)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.9, sx * 4.2))
        m.box(hd, x0, 31.0, -27.0, x1, 32.2, -25.0, solid(P, "eye", glow=True))
        for j in range(3):                                                               # horn crest
            spike(m, hd, (sx * 2.0, 34.0, -24.0 + j * 2.6), (sx * 0.4, 1, 0.6), 1.4, 6.0 - j, headf, tip=0.8)
    for j in range(6):                                                                   # long white mane + beard
        rod(m, hd, (0, 29.0 - j * 0.4, -18.0 + j * 0.4), ((j - 2.5) * 2.0, 22.0 - j * 0.6, -8.0 + j * 2.0), 1,
            strands(P, "white", "white_dark"), extend=0.2, t2=2)
    rod(m, hd, (0, 26.6, -28.0), (0, 18.0, -24.0), 2, strands(P, "white", "white_dark"), extend=0.2, t2=1)
    return m
