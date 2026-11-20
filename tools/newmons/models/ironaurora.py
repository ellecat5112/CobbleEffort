"""Iron Aurora (Ice/Psychic), the future paradox Articuno, built from boxes after the art the user shared (artist not
named, no name given; our name).

A robot Articuno in flight: an egg-shaped body of pale steel-blue plates round a glowing cyan glass belly full of
stars, a little head with a white beak, a blue grid visor and a crest of three starry blue spikes, black speaker discs
on its shoulders, and ball-jointed legs with thin silver shins and black talons. Its wings rise in a V from segmented
steel arms: broad bands of feathers, cyan near the arm and deep blue at their stepped edges, sprinkled with stars.
A long starry blue tail ribbons down below it and ends in a white banded tip.

Shiny: violet plates and a magenta-pink starfield.

Front is -z, y is up. 68 units tall (wings up); about 2.6 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, ribbon, smooth_path, stars, tri, band_wing
from _regi import ellipsoid, lit
from _route import pal, tone

HEIGHT = 68
SCALE = round(2.6 * 16 / HEIGHT, 3)
HITBOX = [1.8, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a robot Articuno with a starry cyan glass belly, a grid visor and starry crest, V-raised wings of cyan and "
        "deep blue feathers on segmented steel arms and a long starry tail ending in a white banded tip")

BASE = {"plate": (150, 196, 244), "plate_dark": (104, 150, 214), "seam": (60, 92, 156), "glass": (72, 206, 250),
        "glass_dark": (40, 150, 224), "star": (255, 255, 255), "navy": (24, 60, 160), "blue": (56, 146, 246),
        "cyan": (96, 226, 255), "white": (236, 242, 250), "beak_tip": (120, 132, 150), "black": (34, 36, 44),
        "grey": (86, 90, 100), "visor": (60, 160, 255), "visor_dark": (24, 60, 130), "silver": (206, 214, 228)}
SHINY = {"plate": (196, 176, 236), "plate_dark": (150, 126, 204), "seam": (90, 60, 150), "glass": (250, 130, 220),
         "glass_dark": (200, 80, 190), "navy": (70, 28, 120), "blue": (150, 70, 220), "cyan": (250, 150, 236),
         "visor": (255, 110, 210), "visor_dark": (110, 30, 100)}
CY = 36.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def bodyf(x, y, z, face, variant, **k):
    """Pale plates; on the front, a glowing cyan glass belly window full of stars, rimmed with a dark seam."""
    p = P(variant)
    e = (x / 3.2) ** 2 + ((y - 34.6) / 5.6) ** 2
    if face == "north" and z < -1.5:
        if e < 1:
            if stars(x, y, z, face, cell=1.3, r=0.26, prob=0.4):
                return p["star"], p["star"]
            c = p["glass"] if e < 0.6 else p["glass_dark"]
            return c, c
        if e < 1.35:
            return lit(p["seam"], face, y, CY, 7), None
    if abs(y - 41.2) < 0.35 or (face in ("east", "west") and abs(z - 1.6) < 0.3 and y < 41):
        return lit(p["seam"], face, y, CY, 7), None
    return lit(p["plate"] if face != "south" else p["plate_dark"], face, y, CY, 7), None


def headf(x, y, z, face, variant, **k):
    """Pale plates with a blue grid visor round the front and sides."""
    p = P(variant)
    if 45.6 < y < 47.6 and face != "up" and face != "down" and (face != "south"):
        u = x if face == "north" else z
        if (u * 3) % 1.0 < 0.22 or ((y - 45.6) * 3) % 1.0 < 0.22:
            return p["visor_dark"], None
        return p["visor"], p["visor"]
    return lit(p["plate"], face, y, 46, 3), None


def beakf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = box.lo[2] + box.size[2] - z if box is not None else 0
    return tone(p["beak_tip"] if d > box.size[2] * 0.7 else p["white"], face), None


def starf(x, y, z, face, variant, **k):
    p = P(variant)
    if stars(x, y, z, face, cell=1.2, r=0.24, prob=0.45):
        return p["star"], p["star"]
    return tone(p["blue"], face), None


def discf(cx, cy, cz):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        r = ((y - cy) ** 2 + (z - cz) ** 2) ** 0.5
        if face in ("east", "west"):
            if r < 0.7:
                return p["grey"], None
            if 1.4 < r < 1.8:
                return p["grey"], None
        return tone(p["black"], face), None
    return s


def tailf(x, y, z, face, variant, **k):
    p = P(variant)
    if stars(x, y, z, face, cell=1.5, r=0.28, prob=0.4):
        return p["star"], p["star"]
    return tone(p["blue"] if face != "south" else p["navy"], face), None


def tipf(x, y, z, face, variant, **k):
    """The white banded tail tip (rods: z runs along the rod)."""
    p = P(variant)
    return tone(p["white"] if (z % 1.6) < 1.1 else p["plate_dark"], face), None


def wing_shader(curve, width):
    def sh(x, y, z, face, variant, u=0.0, **k):
        p = P(variant)
        t, s, lat = curve.locate(u, y)
        if lat > 0.9:
            return CLEAR
        w = width(t) * (1 - 0.26 * ((t * 6) % 1.0))                  # stepped outer edge
        if s < -0.6 or s > w or w <= 0.2:
            return CLEAR
        f = max(0.0, s) / max(w, 0.01)
        if w - s < 0.7:
            return p["navy"], None                                       # the dark outline
        if f < 0.42 + 0.16 * tri(t * 6):                                 # cyan near the arm, chevroned
            key = "cyan"
        else:
            key = "blue"
        if stars(u, y, 0, "north", cell=1.6, r=0.28, prob=0.36):
            return p["star"], p["star"]
        return (p[key], p[key]) if key == "cyan" else (p[key], None)
    return sh


def width(t):
    import math
    return 11.5 * max(0.0, math.sin(math.pi * (0.12 + 0.88 * t))) ** 0.7


ARM = [(4.0, 40.5), (16.0, 43.0), (26.0, 55.0), (23.0, 68.0)]


def build() -> Model:
    m = Model("ironaurora")
    top = m.bone("ironaurora", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY, 0.4, 4.6, 7.6, 4.4, bodyf, step=1)                  # the egg body
    rod(m, bd, (0, 41.5, 0), (0, 44.5, -0.3), 3, solid("plate_dark"), extend=0.4)  # neck
    for sx in (-1, 1):                                                          # shoulder speaker discs
        x0, x1 = sorted((sx * 4.2, sx * 5.2))
        m.box(bd, x0, 37.4, -1.4, x1, 40.6, 1.4, discf(0, 39, 0))
        m.box(bd, x0 + 0.05 * sx, 37.9, -1.9, x1 - 0.05 * sx, 40.1, 1.9, discf(0, 39, 0))
    hd = m.bone("head", bd, (0, 44, 0))
    m.round_box(hd, 0, -0.6, 2.9, 3.2, 43.6, 49.0, headf, cut=1)                # head
    rod(m, hd, (0, 46.0, -3.4), (0, 44.6, -8.2), 1.8, beakf, extend=0.3, t2=1.4)  # beak
    spike(m, hd, (0, 48.4, -0.4), (0, 1, 0.3), 1.8, 5.6, starf, tip=0.9)       # starry crest
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.3, 48.0, 0.2), (sx * 0.55, 1, 0.45), 1.4, 4.2, starf, tip=0.8)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                      # wings on segmented arms
        wg = m.bone(nm, bd, (sx * 4, 40.5, 0.8))
        c = band_wing(m, wg, sx, ARM, width, 1.2, wing_shader, (3.0, 31.0, 30.0, 69.0))
        knots = [c.at(t) for t in (0.0, 0.22, 0.45, 0.66, 0.8)]
        for a, b in zip(knots, knots[1:]):
            rod(m, wg, (sx * a[0], a[1], 0.8), (sx * b[0], b[1], 0.8), 2.2, solid("plate"), extend=0.2)
        for kx, ky in knots[1:-1]:
            m.box(wg, sx * kx - 1.4, ky - 1.4, -0.6, sx * kx + 1.4, ky + 1.4, 2.2, solid("plate_dark"))
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, bd, (sx * 2.6, 29.5, -0.8))
        ellipsoid(m, lg, sx * 2.6, 28.8, -0.8, 2.3, 2.3, 2.3, solid("plate"), step=1)   # ball thighs
        knee, ank = (sx * 2.9, 24.6, -3.6), (sx * 3.1, 21.6, -6.4)
        rod(m, lg, (sx * 2.6, 27.0, -1.2), knee, 1.0, solid("silver"), extend=0.4)
        rod(m, lg, knee, ank, 1.0, solid("silver"), extend=0.4)
        m.box(lg, knee[0] - 0.7, knee[1] - 0.7, knee[2] - 0.7, knee[0] + 0.7, knee[1] + 0.7, knee[2] + 0.7,
              solid("grey"))
        for d in ((-0.45, -0.7, -1), (0, -0.8, -1), (0.45, -0.7, -1), (0, -0.4, 1)):
            spike(m, lg, ank, (d[0] * sx, d[1], d[2]), 0.8, 2.4, solid("black"), tip=0.5)
    tl = m.bone("tail", bd, (1.5, 29.5, 3.0))
    spike(m, tl, (1.0, 29.4, 3.2), (1.0, -0.05, 0.3), 2.2, 7.0, solid("white"), tip=1.0)   # white tail fin
    path = smooth_path([(2.0, 29.0, 3.6), (6.5, 25.0, 4.6), (6.0, 19.0, 5.0), (4.5, 13.0, 5.0),
                        (6.5, 7.0, 5.0), (11.0, 3.4, 5.0), (16.5, 2.4, 5.0)], 16)
    ribbon(m, tl, path, [3.4 - 1.0 * i / len(path) for i in range(len(path))], tailf)
    rod(m, tl, (16.0, 2.4, 5.0), (22.5, 3.0, 5.0), 2.2, tipf, extend=0.4)           # white banded tip
    spike(m, tl, (22.0, 3.0, 5.0), (1.0, 0.1, 0), 1.6, 2.0, solid("white"))
    return m
