"""Iron Renegade (Ghost/Steel), the future paradox Giratina, built from boxes after the art the user shared (artist
and name not given; our name).

A towering robot Giratina of violet armour on six spiked black legs, its tall neck and chest striped in black and
yellow chevrons, its armour seamed with glowing pink. Rows of steel spikes run up its neck and along its sides, its
violet helmet carries Giratina's golden mask, and a long violet tail banded in black trails behind. At its back a
great burst of pink energy flares out in jagged rays, glowing yellow at its heart and flinging yellow shards.

Shiny: teal armour with a blue-white burst.

Front is -z, y is up. 60 units tall (to the burst); about 5.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import slab_z
from _pgen1 import CLEAR, smooth_path, stars
from _regi import _hash, ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 60
SCALE = round(5.6 * 16 / HEIGHT, 3)
HITBOX = [3.2, 52 / 16]
KIND = "quadruped"
K = 3
LOOK = ("a towering violet robot Giratina striped in black and yellow chevrons, with steel spikes up its neck, six "
        "spiked black legs, a golden mask and a jagged pink burst of energy flaring at its back")

BASE = {"violet": (126, 60, 160), "violet_dark": (84, 36, 116), "violet_light": (170, 110, 200), "black": (34, 30, 40),
        "yellow": (246, 226, 120), "seam": (255, 120, 170), "steel": (176, 172, 196), "steel_dark": (120, 116, 140),
        "gold": (236, 196, 70), "eye": (230, 40, 40), "burst": (246, 130, 170), "burst_core": (255, 236, 150),
        "shard": (238, 214, 96), "star": (255, 255, 255)}
SHINY = {"violet": (40, 140, 150), "violet_dark": (24, 96, 106), "violet_light": (100, 196, 200),
         "seam": (120, 236, 255), "burst": (130, 190, 250), "burst_core": (230, 246, 255)}
BY = 16.0
NECK = [(0, 20.0, -8.0), (0, 30.0, -11.0), (0, 40.0, -12.0), (0, 47.0, -12.0)]
BC = (0.0, 38.0, 2.0)     # the burst's centre


def P(v):
    return pal(BASE, SHINY, v)


def armourf(x, y, z, face, variant, **k):
    """Violet armour seamed with glowing pink."""
    p = P(variant)
    if abs(math.sin(x * 0.6 + y * 0.25) + math.sin(z * 0.4 - y * 0.3)) < 0.07:
        return p["seam"], p["seam"]
    if face == "up":
        return p["violet_light"], None
    return lit(p["violet"], face, y, BY, 10), None


def chevronf(x, y, z, face, variant, box=None, **k):
    """The neck: black and yellow chevrons down its front, violet behind (rods pointing up show their local "down"
    face to the front; x and y are centred on the rod's start, z runs back from it)."""
    p = P(variant)
    if face == "down":
        u = x - (box.lo[0] + box.size[0] / 2)
        yy = box.lo[1] + box.size[1] / 2 + (box.lo[2] + box.size[2] - z)
        w = (yy + abs(u) * 0.9) % 6.0
        return ((p["yellow"] if w < 2.6 else p["black"]), None)
    return armourf(x, y, z, face, variant)


def bodyf(x, y, z, face, variant, **k):
    """The body: its chest striped like the neck, violet armour elsewhere."""
    p = P(variant)
    if face == "north":
        w = (y + abs(x) * 0.9) % 6.0
        return ((p["yellow"] if w < 2.6 else p["black"]), None)
    return armourf(x, y, z, face, variant)


def blackf(x, y, z, face, variant, **k):
    return tone(P(variant)["black"], face), None


def steelf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["steel"] if face != "down" else p["steel_dark"], face), None


def goldf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["gold"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 15.4, y - 48.6) < 0.8:
        return p["eye"], p["eye"]
    return armourf(x, y, z, face, variant)


def burstf(x, y, z, face, variant, **k):
    """A jagged burst of pink energy (an xy plane), glowing yellow at its heart, flecked with sparks."""
    p = P(variant)
    dx, dy = x - BC[0], y - BC[1]
    r = math.hypot(dx, dy)
    a = math.atan2(dy, dx)
    n = 14
    f = (a / (2 * math.pi) * n) % 1.0
    i = int(math.floor(a / (2 * math.pi) * n)) % n
    R = 13.0 + 7.0 * _hash(i, 9) * (1 - abs(2 * f - 1)) ** 1.5 + 3.0 * (1 - abs(2 * f - 1))
    if r > R:
        return CLEAR
    if r < R * 0.55 and (1 - abs(2 * ((a / (2 * math.pi) * n * 2) % 1.0) - 1)) > r / (R * 0.55):
        return p["burst_core"], p["burst_core"]
    if stars(x, y, z, face, cell=1.6, r=0.2, prob=0.25):
        return p["star"], p["star"]
    return p["burst"], p["burst"]


def shardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
    u, v = abs(x - cx) / (box.size[0] / 2), (y - box.lo[1]) / box.size[1]
    if u > math.sin(math.pi * v) ** 0.6 * (1 - v * 0.4):
        return CLEAR
    return p["shard"], p["shard"]


def build() -> Model:
    m = Model("ironrenegade")
    top = m.bone("ironrenegade", None, (0, 0, 0))
    bd = m.bone("body", top, (0, BY, 0))
    for z0, z1, rx, ry in ((-12, -6, 6.6, 6.0), (-6, 0, 7.0, 6.2), (0, 6, 6.8, 6.0), (6, 12, 6.0, 5.4)):
        slab_z(m, bd, 0, BY, z0, z1, rx, ry, bodyf if z0 < -10 else armourf)       # the body
    nk = m.bone("neck", bd, NECK[0])
    pts = smooth_path(NECK, 8)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        w = 8.4 - 3.0 * i / (len(pts) - 2)
        rod(m, nk, a, b, round(w * 2) / 2, chevronf, extend=0.8)
        for sx in (-1, 1):                                                       # steel spikes up its neck
            if i % 2 == 0:
                spike(m, nk, (sx * w * 0.45, a[1], a[2] + 1.0), (sx * 1, 0.5, 0.5), 2.0, 5.0 - i * 0.3, steelf, tip=0.8)
    hd = m.bone("head", nk, (0, 47.0, -12.0))                                       # violet helmet, golden mask
    m.round_box(hd, 0, -13.0, 3.6, 4.0, 45.6, 51.4, headf, cut=1)
    m.round_box(hd, 0, -17.0, 2.6, 2.6, 45.6, 49.6, headf, cut=0.6)
    m.box(hd, -1.4, 50.0, -18.6, 1.4, 53.6, -12.0, goldf)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 1.4, sx * 4.4))
        m.box(hd, x0, 46.4, -17.6, x1, 52.2, -12.4, goldf, rotation=(0, sx * 12, 0), pivot=(sx * 2.4, 49.0, -15.0))
        spike(m, hd, (sx * 3.2, 51.4, -11.0), (sx * 0.5, 1, 0.6), 2.0, 5.6, armourf, tip=0.8)   # helmet horns
    for sx in (-1, 1):                                                           # spikes along its sides
        for i, z in enumerate((-8.0, -2.0, 4.0, 10.0)):
            spike(m, bd, (sx * 6.4, BY + 3.0, z), (sx * 1, 0.6, 0.3), 2.2, 4.4, steelf, tip=0.8)
    for nm, sx, z in (("leg_front_left", 1, -9.0), ("leg_front_right", -1, -9.0), ("leg_mid_left", 1, 0.0),
                      ("leg_mid_right", -1, 0.0), ("leg_back_left", 1, 9.0), ("leg_back_right", -1, 9.0)):
        hip = (sx * 6.6, BY - 2.0, z)
        lg = m.bone(nm, top, hip)
        ellipsoid(m, lg, hip[0] + sx * 0.6, hip[1] - 2.4, z, 3.4, 4.4, 3.4, armourf, step=1)
        rod(m, lg, (sx * 7.2, 9.0, z), (sx * 7.6, 1.6, z - 0.6), 4.4, blackf, extend=0.6)
        m.box(lg, sx * 7.6 - 2.6, 0, z - 3.0, sx * 7.6 + 2.6, 2.6, z + 1.6, blackf)
        for c in (-1, 0, 1):
            spike(m, lg, (sx * 7.6 + c * 1.6, 1.0, z - 2.8), (c * 0.35, -0.2, -1), 1.4, 2.8, steelf, tip=0.6)
        spike(m, lg, (sx * 9.4, 8.0, z), (sx * 1, 0.8, 0), 1.8, 3.4, steelf, tip=0.6)
    tl = m.bone("tail", bd, (0, BY, 12.0))
    tpts = smooth_path([(0, BY, 11.0), (2.0, BY - 3.0, 18.0), (6.0, BY - 7.0, 24.0), (12.0, BY - 9.0, 28.0),
                        (18.0, BY - 8.0, 31.0)], 10)
    for i, (a, b) in enumerate(zip(tpts, tpts[1:])):
        rod(m, tl, a, b, max(1.0, round((5.6 - 4.4 * i / (len(tpts) - 2)) * 2) / 2),
            blackf if i % 3 == 1 else armourf, extend=0.8)
    burst = m.bone("cap", bd, BC)                                                  # the burst of energy at its back
    R = 23.0
    m.box(burst, BC[0] - R, max(8.0, BC[1] - R), BC[2] + 4.0, BC[0] + R, min(60.0, BC[1] + R), BC[2] + 4.0, burstf)
    for i in range(8):                                                           # yellow shards flung from it
        a = math.radians(i * 45 + 20)
        c = (BC[0] + math.cos(a) * 16.0, BC[1] + math.sin(a) * 15.0)
        if 10.0 < c[1] < 58.0:
            m.box(burst, c[0] - 1.0, c[1] - 1.6, BC[2] + 3.0, c[0] + 1.0, c[1] + 1.6, BC[2] + 3.0, shardf)
    return m
