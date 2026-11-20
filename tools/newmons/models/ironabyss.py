"""Iron Abyss (Fairy/Water), the future paradox Manaphy, built from boxes after @pokefeast's art (the art's own name).

A Manaphy of glassy cyan jelly with bubbles caught inside. Its big round head is a clear dome with a darker rim, its
eyes are round yellow-rimmed lenses with a grid inside, ringed with little yellow lights, over a happy pink mouth. A
red gem glows on its chest. Its arm fins are white panels traced with cyan circuits, one raised high, and two long
cyan antennae flow from the back of its head down to glowing balls by its feet. A faint rainbow ring hangs behind it.

Shiny: pink jelly with mint fins.

Front is -z, y is up. 27 units tall; about 0.9 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, rainbow, smooth_path, stars
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 27
SCALE = round(0.9 * 16 / HEIGHT, 3)
HITBOX = [0.8, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = ("a Manaphy of glassy cyan jelly with yellow-rimmed grid lens eyes, a red chest gem, white circuit fins and two "
        "long antennae flowing down to glowing balls, before a faint rainbow ring")

BASE = {"jelly": (120, 216, 226), "jelly_dark": (70, 170, 190), "jelly_light": (200, 244, 248), "rim": (60, 150, 176),
        "lens": (90, 170, 220), "lens_grid": (40, 110, 170), "yellow": (246, 214, 80), "mouth": (240, 140, 180),
        "gem": (220, 40, 50), "white": (246, 248, 252), "circuit": (70, 190, 210), "ball": (170, 240, 200),
        "bubble": (240, 255, 255)}
SHINY = {"jelly": (240, 160, 200), "jelly_dark": (200, 110, 160), "jelly_light": (255, 220, 236), "rim": (180, 90, 140),
         "circuit": (110, 220, 170), "ball": (255, 200, 230)}
HY = 18.0
RC = (0.0, 15.0, 4.0)       # the rainbow ring's centre


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def headf(x, y, z, face, variant, **k):
    """The jelly dome: bubbles inside, a darker rim at its base; lens eyes, little lights and a smile on its front."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 2.4, y - (HY + 0.2)
            r = math.hypot(dx, dy)
            if r < 1.5:
                return (p["lens_grid"] if (dx % 0.7 < 0.18 or dy % 0.7 < 0.18) else p["lens"]), None
            if r < 2.0:
                return p["yellow"], None
            for a in (60, 100):
                q = math.radians(a if sx > 0 else 180 - a)
                if math.hypot(dx - math.cos(q) * 2.8, dy - math.sin(q) * 2.8) < 0.45:
                    return p["yellow"], p["yellow"]
        if abs(x) < 1.2 and -3.2 < y - HY < -2.0 and (y - HY + 2.0) < -0.6 * (1 - (x / 1.2) ** 2) * 2:
            return p["mouth"], None
    if y < HY - 4.0:
        return tone(p["rim"], face), None
    if stars(x, y, z, face, cell=1.4, r=0.22, prob=0.22):
        return p["bubble"], None
    if face == "up":
        return p["jelly_light"], None
    return lit(p["jelly"], face, y, HY, 5), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, (y - 10.4) * 0.7) < 0.8:
        return p["gem"], p["gem"]
    if face == "north" and math.hypot(x, y - 8.6) < 0.35:
        return p["yellow"], None
    return lit(p["jelly"], face, y, 10, 3), None


def finf(x, y, z, face, variant, box=None, **k):
    """A white fin panel traced with cyan circuits (rods: x across, z along from the root)."""
    p = P(variant)
    cx = box.lo[0] + box.size[0] / 2
    d = box.lo[2] + box.size[2] - z
    if face in ("up", "down") and (abs(x - cx) < 0.3 and d < box.size[2] * 0.7 or abs(d - box.size[2] * 0.4) < 0.3):
        return p["circuit"], p["circuit"]
    return tone(p["white"], face), None


def ringf(x, y, z, face, variant, **k):
    """A faint rainbow ring (an xy plane)."""
    dx, dy = x - RC[0], y - RC[1]
    r = math.hypot(dx, dy)
    if abs(r - 11.0) > 0.6:
        return CLEAR
    c = rainbow(math.atan2(dy, dx) / (2 * math.pi), s=0.35)
    return c + (140,), c


def build() -> Model:
    m = Model("ironabyss")
    top = m.bone("ironabyss", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10.0, 0))
    ellipsoid(m, bd, 0, 10.0, 0.2, 3.0, 3.4, 2.8, bodyf, step=1)                     # little jelly body
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, bd, (sx * 1.4, 7.0, 0.2))
        ellipsoid(m, lg, sx * 1.6, 6.0, 0.0, 1.3, 1.6, 1.3, solid("jelly"), step=1)
    hd = m.bone("head", bd, (0, 13.0, 0))
    ellipsoid(m, hd, 0, HY, 0.0, 6.0, 5.2, 5.6, headf, step=1)                       # the clear dome head
    for nm, sx, up in (("arm_left", 1, True), ("arm_right", -1, False)):          # white circuit fins
        ar = m.bone(nm, bd, (sx * 2.6, 12.0, 0))
        a0 = (sx * 2.6, 12.0, 0.0)
        a1 = (sx * 7.0, 15.4 if up else 9.6, -0.6)
        a2 = (sx * 10.6, 20.0 if up else 6.4, -0.8)
        rod(m, ar, a0, a1, 1.2, finf, extend=0.4, t2=3.6)
        rod(m, ar, a1, a2, 1.2, finf, extend=0.4, t2=4.6)
    for nm, sx in (("antenna_left", 1), ("antenna_right", -1)):                  # long flowing antennae
        an = m.bone(nm, hd, (sx * 2.0, HY + 4.0, 3.0))
        pts = smooth_path([(sx * 2.0, HY + 4.0, 3.0), (sx * 6.0, HY + 7.0, 5.6), (sx * 10.0, HY + 2.0, 6.4),
                           (sx * 11.4, 9.0, 5.0), (sx * 11.6, 3.4, 3.0)], 12)
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            rod(m, an, a, b, round((2.0 - 0.6 * i / (len(pts) - 2)) * 2) / 2, solid("jelly"), extend=0.4)
        e = pts[-1]
        ellipsoid(m, an, e[0], e[1] - 0.8, e[2], 1.8, 1.8, 1.8, solid("ball", True), step=1)
    rg = m.bone("ring_rainbow", top, RC)                                             # faint rainbow ring
    m.box(rg, RC[0] - 11.8, RC[1] - 11.8, RC[2], RC[0] + 11.8, RC[1] + 11.8, RC[2], ringf)
    return m
