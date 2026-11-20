"""Iron Pyre (Fire/Electric), the future paradox Moltres, built from boxes after the art the user shared (artist not
named, no name given; our name).

A lean robot Moltres in flight: a gold egg of a body with a red and orange flame chevron down its front, a neck of
silver rings banded in red, a gold head with a long pointed silver beak, a red grid visor and a crest of glowing
flame. Its wings are long gold arms of five segments raised in a V, with jagged sheets of glowing flame hanging from
them, red at the edges, orange near the arm and laced with pale fire, sprinkled with sparks. Gold ball thighs, thin
silver shins with grey talons, black speaker discs on its shoulders, and a tail of flame.

Shiny: a silver body and blue fire.

Front is -z, y is up. 65 units tall (wings up); about 2.8 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, band_wing, stars, tri
from _regi import ellipsoid, lit
from _route import pal, tone

HEIGHT = 65
SCALE = round(2.8 * 16 / HEIGHT, 3)
HITBOX = [1.8, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a lean robot Moltres with a gold egg body, a ringed silver neck, a long silver beak and red grid visor, "
        "segmented gold wing arms hung with jagged glowing flame and a tail of fire")

BASE = {"gold": (240, 214, 150), "gold_dark": (196, 166, 100), "seam": (150, 116, 60), "silver": (196, 204, 222),
        "silver_dark": (130, 140, 162), "red": (206, 52, 78), "red_dark": (150, 30, 54), "orange": (252, 156, 116),
        "pale": (255, 228, 176), "spark": (255, 255, 255), "visor": (230, 40, 60), "visor_dark": (90, 10, 20),
        "black": (34, 34, 40), "grey": (90, 94, 104), "talon": (60, 60, 70)}
SHINY = {"gold": (214, 218, 232), "gold_dark": (164, 170, 192), "seam": (110, 116, 140), "red": (44, 98, 226),
         "red_dark": (24, 56, 160), "orange": (92, 190, 252), "pale": (206, 244, 255), "visor": (60, 170, 255),
         "visor_dark": (10, 40, 90)}
CY = 32.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def flame_colour(p, f, t):
    """Across a flame sheet: f = 0 at the root, 1 at the edge."""
    if f > 0.86:
        return p["red_dark"]
    if f > 0.5 + 0.12 * tri(t * 7):
        return p["red"]
    if abs(f - (0.32 + 0.1 * tri(t * 11))) < 0.05:
        return p["pale"]
    return p["orange"]


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and z < -1.0:
        edge = 33.5 - 2.4 * tri(x / 2.2 + 0.5)                         # zigzag top of the flame chevron
        if y < edge and y > 24.8 + abs(x) * 0.9:
            c = p["orange"] if y < edge - 1.6 else p["red"]
            return c, c
    if abs(y - 37.6) < 0.3:
        return lit(p["seam"], face, y, CY, 8), None
    return lit(p["gold"] if face != "south" else p["gold_dark"], face, y, CY, 8), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if 45.6 < y < 47.2 and face in ("north", "east", "west"):
        u = x if face == "north" else z
        if (u * 3) % 1.0 < 0.25 or ((y - 45.6) * 3) % 1.0 < 0.25:
            return p["visor_dark"], None
        return p["visor"], p["visor"]
    return lit(p["gold"], face, y, 46, 3), None


def beakf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = box.lo[2] + box.size[2] - z
    return tone(p["silver_dark"] if d > box.size[2] * 0.75 or face == "down" else p["silver"], face), None


def neckf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["red"] if (z % 1.5) < 0.4 else p["silver"], face), None


def discf(x, y, z, face, variant, **k):
    p = P(variant)
    r = ((y - 40.0) ** 2 + z ** 2) ** 0.5
    if face in ("east", "west") and (r < 0.7 or 1.4 < r < 1.8):
        return p["grey"], None
    return tone(p["black"], face), None


def wing_shader(curve, width):
    def sh(x, y, z, face, variant, u=0.0, **k):
        p = P(variant)
        t, s, lat = curve.locate(u, y)
        if lat > 0.9:
            return CLEAR
        w = width(t) * (0.62 + 0.38 * tri(t * 7 + 0.5) ** 1.5)              # flame tongues
        if s < -0.5 or s > w or w <= 0.2:
            return CLEAR
        if stars(u, y, 0, "north", cell=1.9, r=0.3, prob=0.3):
            return p["spark"], p["spark"]
        c = flame_colour(p, max(0.0, s) / max(width(t), 0.01), t)
        return c, c
    return sh


def width(t):
    return 2.0 + 13.5 * max(0.0, math.sin(math.pi * (0.12 + 0.88 * t))) ** 0.8


ARM = [(3.6, 42.0), (11.0, 48.0), (19.0, 57.0), (26.0, 64.5)]


def radial_flame(cx, cy, a0, a1, r_in, r_out, n):
    """A fan of n flame tongues round (cx, cy) between angles a0..a1 (degrees, 0 = up, clockwise toward -x)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        dx, dy = cx - x, y - cy
        a = math.degrees(math.atan2(dx, dy))
        if not (a0 <= a <= a1):
            return CLEAR
        f = (a - a0) / (a1 - a0)
        R = r_in + (r_out - r_in) * (0.42 + 0.58 * tri(f * n + 0.5) ** 1.4) * (0.6 + 0.4 * math.sin(math.pi * f))
        r = math.hypot(dx, dy)
        if r > R:
            return CLEAR
        if stars(x, y, 0, "north", cell=1.7, r=0.28, prob=0.3):
            return p["spark"], p["spark"]
        c = flame_colour(p, r / max(R, 0.01), f)
        return c, c
    return s


def build() -> Model:
    m = Model("ironpyre")
    top = m.bone("ironpyre", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY + 0.8, 0.4, 3.9, 6.8, 3.7, bodyf, step=1)                     # the gold egg body
    for i in range(3):                                                             # ringed silver neck
        a, b = (0, 39.0 + i * 1.6, 0.2 - i * 0.4), (0, 40.6 + i * 1.6, -0.2 - i * 0.4)
        rod(m, bd, a, b, 2.6 - 0.2 * i, neckf, extend=0.4)
    for sx in (-1, 1):                                                             # speaker discs
        x0, x1 = sorted((sx * 3.8, sx * 4.8))
        m.box(bd, x0, 38.4, -1.4, x1, 41.6, 1.4, discf)
        m.box(bd, x0 + 0.05 * sx, 38.9, -1.9, x1 - 0.05 * sx, 41.1, 1.9, discf)
    hd = m.bone("head", bd, (0, 44.5, -1))
    m.round_box(hd, 0, -1.0, 2.4, 2.8, 44.2, 48.6, headf, cut=1)                  # gold head
    rod(m, hd, (0, 46.2, -3.4), (0, 45.0, -9.6), 1.6, beakf, extend=0.3, t2=1.4)    # long silver beak
    rod(m, hd, (0, 45.1, -9.2), (0, 44.6, -11.6), 0.8, beakf, extend=0.2)
    m.box(hd, -6, 44, 0.8, 6, 56, 0.8, radial_flame(0, 46, -70, 70, 2.0, 9.0, 5))   # flame crest (front)
    m.box(hd, 0, 44, -2.0, 0, 55, 6.0, radial_flame_side())                        # flame crest (side)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):
        wg = m.bone(nm, bd, (sx * ARM[0][0], ARM[0][1], 0.8))
        c = band_wing(m, wg, sx, ARM, width, 1.0, wing_shader, (3.0, 36.0, 22.0, 66.0))
        knots = [c.at(t) for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)]
        for a, b in zip(knots, knots[1:]):
            rod(m, wg, (sx * a[0], a[1], 0.8), (sx * b[0], b[1], 0.8), 1.8, solid("gold"), extend=0.0)
        for kx, ky in knots[1:-1]:
            m.box(wg, sx * kx - 1.1, ky - 1.1, -0.3, sx * kx + 1.1, ky + 1.1, 1.9, solid("gold_dark"))
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, bd, (sx * 2.6, 27, -0.5))
        ellipsoid(m, lg, sx * 2.6, 26.2, -0.6, 2.4, 2.6, 2.4, solid("gold"), step=1)   # ball thighs
        knee, ank = (sx * 2.8, 20.8, -2.2), (sx * 2.9, 16.4, -3.2)
        rod(m, lg, (sx * 2.6, 24.0, -0.8), knee, 1.0, solid("silver"), extend=0.4)
        rod(m, lg, knee, ank, 1.0, solid("silver"), extend=0.4)
        m.box(lg, knee[0] - 0.7, knee[1] - 0.7, knee[2] - 0.7, knee[0] + 0.7, knee[1] + 0.7, knee[2] + 0.7,
              solid("grey"))
        for d in ((-0.45, -0.8, -1), (0, -0.9, -1), (0.45, -0.8, -1), (0, -0.5, 1)):
            spike(m, lg, ank, (d[0] * sx, d[1], d[2]), 0.8, 2.6, solid("talon"), tip=0.5)
    tl = m.bone("tail", bd, (0, 25, 2))
    m.box(tl, -14, 6, 2.2, 6, 26, 2.2, radial_flame(0, 25.5, 120, 205, 3.0, 17.0, 5))   # tail of flame
    return m


def radial_flame_side():
    """The crest seen from the side: tongues sweeping back from the head (a yz plane at x = 0)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        dz, dy = z - (-0.5), y - 46.0
        a = math.degrees(math.atan2(dz, dy))                            # 0 = up, 90 = back
        if not (-10 <= a <= 110):
            return CLEAR
        f = (a + 10) / 120
        R = 2.5 + 7.0 * (0.4 + 0.6 * tri(f * 4 + 0.5) ** 1.3)
        r = math.hypot(dz, dy)
        if r > R:
            return CLEAR
        c = flame_colour(p, r / max(R, 0.01), f)
        return c, c
    return s
