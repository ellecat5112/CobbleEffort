"""Iron Eon (Steel/Psychic), the future paradox Latios, built from boxes after Glowing_Shark's art (the art's own name).

A Latios rebuilt as a jet: a sleek violet-blue fuselage banded in navy and silver, a cyan glass canopy, broad swept
delta wings with white tips, two engine pods and three tall swept fins wreathed in glowing cyan afterburn. Its head
juts low at the nose with a yellow eye ringed in cyan on each side and two long hooked horns curving down past its
chin.

Shiny: a silver fuselage with crimson bands.

Front is -z, y is up. 29 units tall (to the fins); about 1.6 blocks tall and 2.8 long.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import slab_z
from _pgen1 import CLEAR, inside
from _regi import ellipsoid
from _route import pal, tone

HEIGHT = 29
SCALE = round(1.6 * 16 / HEIGHT, 3)
HITBOX = [2.4, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a jet-shaped violet-blue Latios with navy bands, a cyan canopy, swept white-tipped delta wings, engine pods, "
        "three tall fins in glowing cyan afterburn and long hooked horns at its nose")

BASE = {"violet": (96, 92, 222), "violet_light": (140, 136, 240), "navy": (36, 36, 92), "white": (232, 236, 246),
        "silver": (190, 196, 214), "cyan": (90, 220, 255), "cyan_light": (200, 246, 255), "eye": (250, 220, 60),
        "pupil": (30, 26, 40)}
SHINY = {"violet": (196, 200, 216), "violet_light": (226, 230, 240), "navy": (150, 30, 50), "cyan": (255, 120, 150),
         "cyan_light": (255, 214, 224)}
CY = 12.0
WING = [(3.0, -6.0), (22.0, 11.0), (21.0, 15.0), (3.0, 14.0)]
CANARD = [(3.0, -12.0), (9.0, -5.0), (9.0, -3.5), (3.0, -6.0)]


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def hullf(x, y, z, face, variant, **k):
    """Violet-blue hull banded in navy, with silver flanks low down."""
    p = P(variant)
    if (z % 7.0) < 1.2:
        return tone(p["navy"], face), None
    if face in ("east", "west") and y < CY - 1.5:
        return tone(p["silver"], face), None
    return tone(p["violet_light"] if face == "up" else p["violet"], face), None


def wingf(poly):
    """A flat wing cut out of a thin box: violet with a navy band and a white tip."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u = abs(x)
        if not inside(poly, u, z):
            return CLEAR
        span = (u - poly[0][0]) / max(1.0, max(q[0] for q in poly) - poly[0][0])
        if span > 0.7:
            return tone(p["white"], face), None
        if abs(span - 0.4) < 0.07:
            return tone(p["navy"], face), None
        return tone(p["violet"] if face != "down" else p["navy"], face), None
    return s


def finf(poly, glow=False):
    """A tall fin on a zy plane: white with a navy band; or (glow) the cyan afterburn behind it."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if not inside(poly, z, y):
            return CLEAR
        if glow:
            return p["cyan"], p["cyan"]
        lo = min(q[1] for q in poly)
        hi = max(q[1] for q in poly)
        f = (y - lo) / max(1.0, hi - lo)
        if 0.35 < f < 0.5:
            return tone(p["navy"], face), None
        return tone(p["white"], face), None
    return s


def headf(x, y, z, face, variant, **k):
    """Navy-and-violet head with a big yellow eye ringed in cyan on each side."""
    p = P(variant)
    if face in ("east", "west"):
        r = math.hypot(z + 16.0, y - 10.2)
        if r < 0.5:
            return p["pupil"], None
        if r < 1.3:
            return p["eye"], None
        if r < 1.8:
            return p["cyan"], p["cyan"]
    return tone(p["navy"] if y > 10.6 else p["violet"], face), None


def build() -> Model:
    m = Model("ironeon")
    top = m.bone("ironeon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    for i, (z0, z1, rx, ry) in enumerate(((-11, -6, 3.6, 3.0), (-6, 0, 4.4, 3.6), (0, 6, 4.8, 3.8), (6, 12, 4.4, 3.4),
                                          (12, 17, 3.6, 2.8), (17, 20, 2.6, 2.0))):
        slab_z(m, bd, 0, CY, z0, z1, rx, ry, hullf)                                  # the fuselage
    ellipsoid(m, bd, 0, CY + 3.4, 1.0, 2.0, 1.6, 3.6, solid("cyan", True), step=1)  # cyan canopy
    for zz in (-1.0, 3.0):
        m.box(bd, -2.1, CY + 3.0, zz - 0.3, 2.1, CY + 5.1, zz + 0.3, solid("white"))
    hd = m.bone("head", bd, (0, CY, -10.0))
    for i, (z0, z1, rx, ry, dy) in enumerate(((-14, -10, 3.6, 3.2, -0.6), (-18, -14, 3.2, 2.8, -1.8),
                                              (-21, -18, 2.4, 2.0, -3.0))):
        slab_z(m, hd, 0, CY + dy, z0, z1, rx, ry, headf)                              # the drooping head
    for sx in (-1, 1):                                                              # long hooked horns
        rod(m, hd, (sx * 1.8, CY + 1.4, -16.0), (sx * 2.6, CY - 3.6, -21.0), 1.0, solid("navy"), extend=0.3)
        rod(m, hd, (sx * 2.6, CY - 3.6, -21.0), (sx * 2.2, CY - 6.4, -18.6), 0.9, solid("navy"), extend=0.3)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):
        wg = m.bone(nm, bd, (sx * 3.0, CY - 1.0, 2.0))
        x0, x1 = sorted((sx * 2.5, sx * 23.0))
        m.box(wg, x0, CY - 1.6, -7.0, x1, CY - 0.4, 16.0, wingf(WING))               # swept delta wings
        x0, x1 = sorted((sx * 2.5, sx * 10.0))
        m.box(wg, x0, CY - 0.6, -13.0, x1, CY + 0.4, -3.0, wingf(CANARD))            # canards
        e = (sx * 7.5, CY - 2.6, 6.0)                                                # engine pods
        rod(m, wg, e, (sx * 7.5, CY - 2.6, 18.0), 2.6, hullf, extend=0.2)
        spike(m, wg, e, (0, 0, -1), 2.6, 3.0, solid("white"), tip=1.2)
        rod(m, wg, (sx * 7.5, CY - 2.6, 18.0), (sx * 7.5, CY - 2.6, 21.0), 1.6, solid("cyan_light", True), extend=0.1)
    fins = m.bone("fins", bd, (0, CY + 3.0, 8.0))
    for x, poly in ((0.0, [(4.0, 15.0), (13.0, 26.0), (15.0, 26.0), (17.0, 15.0)]),
                    (5.5, [(1.0, 14.0), (9.0, 23.0), (11.0, 23.0), (12.0, 14.0)]),
                    (-5.5, [(1.0, 14.0), (9.0, 23.0), (11.0, 23.0), (12.0, 14.0)])):
        m.box(fins, x - 0.5, 13.0, 0.0, x + 0.5, 27.0, 18.0, finf(poly))
        glow = [(poly[0][0] + 2.0, poly[0][1]), (poly[1][0] + 3.0, poly[1][1] + 2.0), (poly[2][0] + 5.0, poly[2][1] + 1.0),
                (poly[3][0] + 4.0, poly[3][1])]
        m.box(fins, x + 0.1, 13.0, 0.0, x + 0.1, 29.0, 22.0, finf(glow, glow=True))
    return m
