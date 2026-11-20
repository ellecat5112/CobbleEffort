"""Gleaming Tide (Water/Rock), the ancient paradox Manaphy, built from boxes after the art the user shared (artist and
name not given; our name).

A Manaphy of deep sea-blue, studded round its head with red gems and crowned with a little knob, from which three
long thin antennae rise, each tipped with a pink bulb marked with a heart. Its eyes are red diamonds set in yellow
stars, and its arm fins and tail are a mosaic of stained-glass shards in pink, orange, teal and white, the tail ending
in a yellow fin.

Shiny: a rose-red body with golden gems.

Front is -z, y is up. 42 units tall (to the antennae); about 1.2 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, inside, smooth_path
from _regi import _hash, ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 42
SCALE = round(1.2 * 16 / HEIGHT, 3)
HITBOX = [0.8, 24 / 16]
KIND = "floater"
K = 4
LOOK = ("a deep blue Manaphy studded with red gems, three long antennae tipped with pink heart bulbs, red diamond eyes "
        "in yellow stars and stained-glass mosaic fins and tail")

BASE = {"blue": (54, 90, 170), "blue_dark": (34, 58, 120), "blue_light": (96, 130, 210), "gem": (210, 40, 60),
        "gem_light": (255, 120, 130), "star": (250, 214, 60), "pink": (240, 120, 170), "pink_light": (255, 200, 220),
        "white": (250, 250, 250), "lead": (40, 40, 60), "fin_yellow": (250, 214, 60),
        "m1": (244, 110, 160), "m2": (250, 170, 80), "m3": (90, 200, 190), "m4": (250, 246, 240), "m5": (250, 220, 90),
        "m6": (230, 70, 110)}
SHINY = {"blue": (190, 60, 80), "blue_dark": (140, 36, 56), "blue_light": (230, 110, 120), "gem": (250, 200, 60),
         "gem_light": (255, 240, 160)}
HY = 18.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def headf(x, y, z, face, variant, **k):
    """The head: deep blue; star eyes with red diamond pupils on its front, a small mouth."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 2.2, y - (HY - 0.4)
            ang = math.atan2(dy, dx)
            r = math.hypot(dx, dy)
            star_r = 1.3 + 0.7 * abs(math.cos(2 * ang)) ** 4
            if abs(dx) * 1.3 + abs(dy) * 0.8 < 0.8:
                return p["gem"], p["gem"]
            if r < star_r:
                return p["star"], None
        if abs(y - (HY - 2.8)) < 0.2 and abs(x) < 0.8 + 0.3 * abs(math.sin(x * 4)):
            return p["lead"], None
    return lit(p["blue"], face, y, HY, 5), None


def mosaic(u, v, p, cell=2.2):
    """A stained-glass shard pattern at (u, v): a colour from the palette, or the dark lead between shards."""
    i, j = math.floor(u / cell), math.floor(v / cell)
    fu, fv = u / cell - i, v / cell - j
    lower = fu + fv < 1.0 if (i + j) % 2 else fu < fv
    edge = min(fu, fv, 1 - fu, 1 - fv, abs(fu + fv - 1.0) / 1.4 if (i + j) % 2 else abs(fu - fv) / 1.4)
    if edge < 0.06:
        return p["lead"]
    keys = ("m1", "m2", "m3", "m4", "m5", "m6")
    return p[keys[int(_hash(i * 2 + lower, j, 7) * 6) % 6]]


def finf(side, poly):
    """An arm fin of stained glass (an xy plane; poly in (u, v), u = side * x)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = side * x
        if not inside(poly, u, y):
            return CLEAR
        return mosaic(u, y, p), None
    return s


def tailf(x, y, z, face, variant, **k):
    p = P(variant)
    u = x if face in ("north", "south") else z
    return mosaic(u + 10.0, y, p, cell=1.2), None


def bulbf(x, y, z, face, variant, box=None, **k):
    """A pink antenna bulb, a white heart on its front."""
    p = P(variant)
    if face == "north":
        cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
        u, v = (x - cx) / 0.9, (y - cy) / 0.9 + 0.2
        if (u * u + v * v - 0.4) ** 3 - u * u * v ** 3 < 0:
            return p["white"], None
    return tone(p["pink"], face), None


def build() -> Model:
    m = Model("gleamingtide")
    top = m.bone("gleamingtide", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 11.0, 0))
    ellipsoid(m, bd, 0, 11.2, 0.4, 2.6, 2.8, 2.4, solid("blue"), step=1)             # little body
    hd = m.bone("head", bd, (0, 14.0, 0))
    ellipsoid(m, hd, 0, HY, 0.0, 5.4, 4.8, 5.0, headf, step=1)                       # the round head
    ellipsoid(m, hd, 0, HY + 4.8, 0.4, 1.6, 1.8, 1.6, solid("blue_light"), step=1)   # crown knob
    ellipsoid(m, hd, 0, HY + 6.4, 0.4, 1.0, 1.0, 1.0, solid("blue_light"), step=1)
    for i in range(8):                                                           # red gems round the head
        a = math.radians(i * 45 + 22.5)
        c = (math.cos(a) * 5.2, HY + 1.6 * math.sin(a * 2), math.sin(a) * 4.8)
        if c[2] < -3.0 and abs(c[0]) < 3.0:
            continue
        ellipsoid(m, hd, c[0], c[1], c[2], 0.8, 0.8, 0.8, solid("gem", True), step=1)
    for j, ctrl in enumerate(([(0, HY + 7.0, 0.4), (0, HY + 12.0, 1.0), (-0.6, HY + 18.0, 0.8), (0, HY + 21.0, 0.2)],
                              [(-0.8, HY + 6.6, 0.4), (-5.0, HY + 9.0, 1.0), (-9.0, HY + 14.0, 0.8), (-9.4, HY + 19.0, 0.4)],
                              [(0.8, HY + 6.6, 0.4), (5.0, HY + 8.6, 1.0), (9.0, HY + 12.0, 0.8), (9.6, HY + 17.0, 0.4)])):
        an = m.bone(f"antenna_{j}", hd, ctrl[0])                                   # three thin antennae
        pts = smooth_path(ctrl, 10)
        for a, b in zip(pts, pts[1:]):
            rod(m, an, a, b, 0.8, solid("blue_dark"), extend=0.4)
        e = pts[-1]
        m.box(an, e[0] - 1.4, e[1], e[2] - 1.2, e[0] + 1.4, e[1] + 2.6, e[2] + 1.2, bulbf)   # pink heart bulb
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                          # stained-glass arm fins
        ar = m.bone(nm, bd, (sx * 2.2, 12.4, 0))
        rod(m, ar, (sx * 2.2, 12.4, 0), (sx * 5.0, 11.0, -0.4), 1.6, solid("blue"), extend=0.4)
        poly = [(4.4, 13.0), (9.6, 13.6), (13.6, 11.2), (12.8, 8.6), (10.4, 9.6), (8.4, 7.4), (6.4, 8.6), (4.4, 10.4)]
        x0, x1 = sorted((sx * 4.2, sx * 13.8))
        m.box(ar, x0, 7.2, -0.4, x1, 13.8, -0.4, finf(sx, poly))
    tl = m.bone("tail", bd, (0, 9.0, 1.0))                                          # mosaic tail, yellow fin
    pts = smooth_path([(0, 9.0, 1.0), (0.6, 6.6, 1.2), (0.6, 4.0, 0.8), (0.2, 2.2, 0.2)], 6)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, a, b, round((2.6 - 1.2 * i / (len(pts) - 2)) * 2) / 2, tailf, extend=0.4)
    for c in (-1, 0, 1):
        spike(m, tl, pts[-1], (c * 0.7, -1, -0.2), 1.0, 2.0, solid("fin_yellow"), tip=0.5)
    return m
