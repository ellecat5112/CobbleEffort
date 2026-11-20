"""Sparkling Verity (Fairy/Psychic), the ancient paradox Mesprit, built from boxes after @Alex_LR04's art (the art's
own name).

A Mesprit with a long red gem horn on its pink head and two long pink ears that droop down past its body like
ribbons, lighter pink inside. Its yellow eyes have red pupils and a fang shows at its grin. A teal mantle spotted
with darker teal hangs from its shoulders down its front, and its two pale tails sweep up round its side, each ending
in three lobes set with red gems.

Shiny: lavender head and ears, violet mantle.

Front is -z, y is up. 30 units tall; about 0.8 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _lake import body, brow_gem, fins, skin, solid, tail
from _pgen1 import CLEAR, inside, smooth_path
from _regi import ellipsoid, lit, speck
from _route import mix, pal, tone

HEIGHT = 30
SCALE = round(0.8 * 16 / HEIGHT, 3)
HITBOX = [0.7, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = ("a Mesprit with a long red gem horn, long drooping pink ears, yellow eyes with red pupils, a teal spotted "
        "mantle and two tails sweeping up round its side, ending in red-gemmed lobes")

BASE = {"skin": (228, 238, 255), "skin_dark": (190, 204, 236), "pink": (240, 146, 176), "pink_dark": (204, 98, 136),
        "pink_light": (252, 196, 214), "red": (220, 40, 52), "red_light": (255, 128, 116), "teal": (80, 168, 176),
        "teal_dark": (34, 100, 118), "teal_light": (150, 214, 220), "line": (130, 140, 176), "eye": (255, 214, 60),
        "pupil": (190, 30, 40), "lid": (70, 40, 60), "fang": (255, 255, 255)}
SHINY = {"pink": (186, 150, 236), "pink_dark": (138, 100, 200), "pink_light": (220, 200, 250), "teal": (130, 96, 186),
         "teal_dark": (80, 50, 130), "teal_light": (190, 160, 230)}
CY = 12.0
HY = 19.4


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, **k):
    """Pink head; on its front two yellow eyes with red slit pupils and dark lids, and a little fanged grin."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = (x - sx * 1.3) * sx, y - (HY - 0.2)
            if dx * dx / 0.95 + dy * dy / 0.75 < 1.0:
                if abs(dx + 0.1) < 0.3 and abs(dy) < 0.65:
                    return p["pupil"], None
                return p["eye"], None
            if -1.0 < dx < 1.1 and 0.75 < dy - 0.35 * dx < 1.05:
                return p["lid"], None
        if abs(y - (HY - 1.9)) < 0.15 and abs(x) < 0.9:
            return p["lid"], None
        if 0.2 < x < 0.6 and HY - 2.5 < y < HY - 1.9:
            return p["fang"], None
    return lit(p["pink"], face, y, HY, 3.2), None


def earf(x, y, z, face, variant, box=None, **k):
    """A long drooping ear: pink, lighter down its middle on its broad faces."""
    p = P(variant)
    if face in ("up", "down"):
        cx = box.lo[0] + box.size[0] / 2
        if abs(x - cx) < box.size[0] * 0.25:
            return p["pink_light"], None
    return tone(p["pink"], face), None


def mantlef(x, y, z, face, variant, **k):
    """The teal mantle down its front (an xy plane): spotted with darker teal, a jagged hem."""
    p = P(variant)
    u = abs(x)
    poly = [(-3.0, 16.4), (2.6, 16.4), (2.8, 13.6), (1.8, 12.4), (1.2, 9.4), (0.2, 10.6), (-0.8, 8.6), (-1.6, 11.6),
            (-2.8, 12.8)]
    if not inside(poly, x, y):
        return CLEAR
    if speck(x, y, 0, "north", cell=1.3, r=0.38, prob=0.5):
        return p["teal_dark"], None
    return tone(p["teal"], face), None


def build() -> Model:
    m = Model("sparklingverity")
    top = m.bone("sparklingverity", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    body(m, bd, CY, P)
    m.box(bd, -3.2, 8.4, -2.8, 3.0, 16.6, -2.8, mantlef)                           # the spotted mantle
    m.round_box(bd, 0, 0.2, 3.2, 2.8, 15.0, 16.6, solid(P, "teal"), cut=1)          # its collar
    fins(m, bd, [(2.6, 16.4), (5.6, 16.0), (7.4, 14.2), (6.0, 13.6), (6.6, 12.0), (4.6, 12.4), (2.6, 14.0)], 0.6, P)
    hd = m.bone("head", bd, (0, 16.8, 0))
    ellipsoid(m, hd, 0, HY, -0.4, 3.3, 3.1, 3.2, headf, step=1)                    # pink head
    brow_gem(m, hd, (0.2, HY + 1.8, -2.8), (0.12, 1, -0.45), P, w=1.6, h=4.4)
    for nm, sx in (("ear_left", 1), ("ear_right", -1)):                           # long drooping ears
        er = m.bone(nm, hd, (sx * 2.2, HY + 2.2, 0.2))
        pts = smooth_path([(sx * 2.2, HY + 2.2, 0.2), (sx * 5.8, HY + 1.6, -0.4), (sx * 8.8, HY - 1.4, -1.0),
                           (sx * 10.2, HY - 5.4, -1.0), (sx * 10.4, HY - 8.6, -0.6)], 10)
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            w = 2.2 + 0.8 * i / (len(pts) - 2)
            rod(m, er, a, b, 1.2, earf, extend=0.6, t2=max(1.5, round(w * 2) / 2))
    tail(m, m.bone("tail_left", bd, (0.8, 9.6, 1.8)),
         [(0.8, 9.6, 1.8), (4.6, 9.4, 3.4), (8.0, 13.0, 3.6), (8.8, 18.6, 2.4), (7.2, 23.0, 1.4), (4.4, 24.4, 0.6)],
         1.8, 1.0, P, lobe=4.4)
    tail(m, m.bone("tail_right", bd, (-0.8, 9.6, 1.8)),
         [(-0.8, 9.6, 1.8), (2.4, 6.6, 3.6), (7.0, 6.6, 3.8), (10.4, 9.0, 2.8), (12.0, 12.6, 1.6)],
         1.8, 1.0, P, lobe=4.4)
    return m
