"""Blossomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a great carnivorous flower. A ring of deep violet petals with white star-burst throats round a round
yellow face with narrow angry eyes and a jagged grin, broad dark green leaves fanned behind, a tangle of thick thorny
green vines for a body, and four of the vines ending in red-petalled biting buds with dark grinning heads.
25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, local, plane, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a great carnivorous flower: a ring of violet petals round a yellow face with angry eyes and a jagged grin, "
        "dark leaves behind, thorny green vines for a body and four red biting buds")
BASE = {"violet": (100, 80, 200), "violet_dark": (44, 30, 110), "violet_light": (190, 180, 250),
        "star": (250, 250, 255), "yellow": (250, 236, 80), "yellow_dark": (210, 180, 30), "mouth": (30, 24, 20),
        "vine": (100, 190, 70), "vine_dark": (40, 110, 30), "thorn": (220, 230, 140), "leaf": (40, 140, 110),
        "leaf_dark": (14, 80, 60), "red": (230, 60, 40), "red_dark": (150, 20, 10), "bud": (70, 70, 80),
        "tooth": (250, 250, 246)}
SHINY = {"violet": (230, 90, 150), "violet_dark": (130, 30, 80), "violet_light": (255, 190, 220),
         "red": (90, 140, 250), "red_dark": (30, 60, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def petalf(key, dark, light, star=False):
    def inside(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        du, t = abs(u / max(W, 1e-6) - 0.5) * 2, v / max(H, 1e-6)
        return du < 0.35 + 0.65 * math.sin(math.pi * min(1.0, t)) ** 0.6 * (1 - 0.6 * t * t)

    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        du, t = abs(u / max(W, 1e-6) - 0.5) * 2, v / max(H, 1e-6)
        if star and t < 0.38 - 0.25 * du and (int(du * 6) % 2 == 0 or t < 0.15):
            return tone(p["star"], face), None
        col = p[light] if du < 0.06 else p[dark] if du > 0.85 else p[key]
        return tone(col, face), None
    return cutout(inside, s)


PETAL = petalf("violet", "violet_dark", "violet_light", star=True)
LEAF = petalf("leaf", "leaf_dark", "vine")
RED = petalf("red", "red_dark", "red", star=False)
VINE = solid(P, "vine")
FC = (0, 30.0, -4.0)


def facef(x, y, z, face, variant, box=None, **k):
    """The yellow face: narrow slanted angry eyes and a jagged black grin."""
    p = P(variant)
    if face == "north":
        a, b = x - FC[0], y - FC[1]
        for sx in (-1, 1):
            if abs(b - 2.4 + sx * a * 0.25 - 0.3) < 0.55 and 1.0 < sx * a < 4.0:
                return tone(p["mouth"], face), None
        zig = -1.4 + 1.2 * abs(((a * 0.8) % 2) - 1)
        if abs(a) < 5.0 and zig - 1.0 < b < zig + 0.3 + 0.8 * (1 - abs(a) / 5):
            return tone(p["mouth"], face), None
    col = p["yellow"] if math.hypot(x - FC[0], y - FC[1]) < 5.4 else p["yellow_dark"]
    return tone(col, face), None


def bud(m, bone, c, d):
    """A red-petalled biting bud: a dark round head with a toothy grin in a ring of red petals."""
    ball(m, bone, c, 2.2, solid(P, "bud"), layers=4)
    for i in range(6):
        spike(m, bone, (c[0] + 1.6 * math.cos(i), c[1] - 0.6, c[2] - 1.6 * math.sin(i)), (0, -1, 0), 0.6, 1.0,
              solid(P, "tooth"))
    for i in range(6):
        ang = i * 60
        m.box(bone, c[0] - 1.6, c[1], c[2] + 1.0, c[0] + 1.6, c[1] + 5.0, c[2] + 1.0, RED,
              rotation=(-50 * d[2], 0, ang), pivot=(c[0], c[1], c[2] + 1.0))


def build():
    m = Model("blossomon")
    top = m.bone("blossomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    # the face: a stacked round disc facing front
    for i in range(3):
        r = 6.6 - i * 1.4
        for fx, fy in ((1.0, 0.42), (0.92, 0.72), (0.72, 0.92), (0.42, 1.0)):
            m.box(bd, -r * fx, FC[1] - r * fy, FC[2] - i * 0.6, r * fx, FC[1] + r * fy, FC[2] + 2.0, facef)
    hd = m.bone("head", bd, FC)
    for i in range(8):                                                    # the ring of violet petals
        ang = i * 45 + 22.5
        m.box(hd, -4.4, FC[1], FC[2] + 1.6, 4.4, FC[1] + 13.0, FC[2] + 1.6, PETAL,
              rotation=(12, 0, ang), pivot=(0, FC[1], FC[2] + 1.6))
    for i in range(7):                                                    # leaves fanned behind
        ang = -70 + i * 23
        m.box(hd, -3.4, FC[1], FC[2] + 6.0, 3.4, FC[1] + 15.0, FC[2] + 6.0, LEAF,
              rotation=(-10, 0, ang), pivot=(0, FC[1] - 3.0, FC[2] + 6.0))
    # the tangle of thorny vines: from under the face down and outward to the ground
    for i in range(10):
        ang = math.radians(i * 36 + 10)
        pts = [(0.6 * math.cos(ang), 24.0, 0.6 * math.sin(ang))]
        for j in range(1, 5):
            r = 2.0 + j * 2.6
            pts.append((r * math.cos(ang + 0.15 * j), 24.0 - j * 5.6 + (j == 4) * 2.0, r * math.sin(ang + 0.15 * j)))
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, bd, p0, p1, 3 if j < 2 else 2, VINE, extend=0.6)
            spike(m, bd, p1, (math.cos(ang), 0.4, math.sin(ang)), 0.6, 1.2, solid(P, "thorn"))
    # four vines reaching out to biting buds
    for k, (sx, sy, sz) in enumerate(((-1, 0.2, -0.4), (1, 0.4, -0.3), (-1, -0.5, -0.6), (1, -0.6, -0.5))):
        bn = m.bone(f"vine_{k}", bd, (0, 24.0, 0))
        tip = (sx * 15.0, 24.0 + sy * 10.0, sz * 10.0)
        mid = (sx * 8.0, 24.0 + sy * 6.0 + 3.0, sz * 6.0)
        rod(m, bn, (0, 24.0, 0), mid, 2, VINE, extend=0.6)
        rod(m, bn, mid, tip, 2, VINE, extend=0.6)
        spike(m, bn, mid, (0, 1, 0), 0.6, 1.2, solid(P, "thorn"))
        bud(m, bn, tip, (sx, sy, sz))
    return m
