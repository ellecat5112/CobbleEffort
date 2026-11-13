"""Shared colours, shaders and the baby builder for the opossum line (Obubby, Mumossum), after the fakemon art by
@Fakemanss that the user shared (the art's own names). `baby()` builds a whole Obubby at any scale, so Mumossum can
carry six little copies of its own baby.

Shiny: dusky purple ears and arms, lavender greys and a lilac tail.
"""
from __future__ import annotations

import math

from _boxmodel import mix, rod
from _route import pal, tone

BASE = {"white": (244, 242, 244), "white_shade": (214, 210, 216), "grey": (172, 168, 176), "grey_dark": (128, 124, 134),
        "ear": (52, 50, 56), "ear_inner": (34, 32, 38), "arm": (44, 42, 48), "snout": (238, 170, 178),
        "nostril": (150, 90, 100), "eye": (40, 30, 30), "glint": (250, 250, 250), "blush": (246, 170, 182),
        "tail": (232, 168, 178), "tail_dark": (200, 132, 146), "foot": (196, 132, 142), "mouth": (110, 40, 52),
        "tongue": (236, 130, 146), "heart": (240, 160, 180), "leg": (56, 52, 60)}
SHINY = {"ear": (110, 80, 140), "ear_inner": (80, 56, 108), "arm": (100, 72, 130), "grey": (184, 166, 210),
         "grey_dark": (140, 120, 172), "tail": (214, 170, 232), "tail_dark": (180, 136, 204), "foot": (196, 150, 220),
         "leg": (96, 70, 126)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def tailf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west", "up") and (abs(x) + abs(y) + abs(z)) % 1.6 < 0.22:
        return tone(p["tail_dark"], face), None                           # ring creases along the tail
    return tone(p["tail"], face), None


def baby_headf(cx, cy, cz, s):
    """A baby's face: big dark eyes, pink blush, white above and a grey band low on the head."""
    def f(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                ex, ey = cx + sx * 1.5 * s, cy + 6.9 * s
                if math.hypot((x - ex) / (0.55 * s), (y - ey) / (0.75 * s)) < 1:
                    if math.hypot(x - ex + 0.2 * s, y - ey - 0.3 * s) < 0.22 * s:
                        return p["glint"], None
                    return p["eye"], None
                if math.hypot((x - cx - sx * 2.4 * s) / (0.6 * s), (y - cy - 5.9 * s) / (0.35 * s)) < 1:
                    return p["blush"], None
        if y < cy + 4.9 * s:
            return tone(p["grey"], face), None
        return tone(p["white"] if face != "down" else p["white_shade"], face), None
    return f


def baby_bodyf(cy, s):
    def f(x, y, z, face, variant, **k):
        p = P(variant)
        if cy + 1.4 * s < y < cy + 2.4 * s:
            return tone(p["grey"], face), None                            # grey band round the middle
        return tone(p["white"] if face != "down" else p["grey_dark"], face), None
    return f


def snoutf(cx, cy, s):
    def f(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if math.hypot((x - cx - sx * 0.35 * s) / (0.18 * s), (y - cy) / (0.25 * s)) < 1:
                    return p["nostril"], None
        return tone(p["snout"], face), None
    return f


def earf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["ear_inner"] if face == "north" else p["ear"], face), None


def baby(m, bone, c, s=1.0, tail=True, mouth_open=False):
    """A whole Obubby with its bottom centre at c, scaled by s, facing -z."""
    cx, cy, cz = c
    m.round_box(bone, cx, cz, 2.3 * s, 2.0 * s, cy + 0.6 * s, cy + 4.2 * s, baby_bodyf(cy, s), cut=max(0.5, 0.8 * s))
    m.round_box(bone, cx, cz, 3.7 * s, 3.3 * s, cy + 3.6 * s, cy + 9.8 * s, baby_headf(cx, cy, cz, s), cut=max(0.5, 1.3 * s))
    m.box(bone, cx - 0.9 * s, cy + 5.6 * s, cz - 3.9 * s, cx + 0.9 * s, cy + 6.8 * s, cz - 3.2 * s, snoutf(cx, cy + 6.2 * s, s))
    for sx in (-1, 1):                                                       # the big dark ears
        m.box(bone, cx + sx * 2.4 * s - 2.1 * s, cy + 8.4 * s, cz - 0.6 * s, cx + sx * 2.4 * s + 2.1 * s,
              cy + 13 * s, cz + 0.6 * s, earf, rotation=(0, 0, sx * 24), pivot=(cx + sx * 2.4 * s, cy + 8.8 * s, cz))
        m.box(bone, cx + sx * 1.6 * s - 0.6 * s, cy + 2 * s, cz - 2.6 * s, cx + sx * 1.6 * s + 0.6 * s,
              cy + 3.8 * s, cz - 1.4 * s, solid("arm"))                       # little dark arms
        m.box(bone, cx + sx * 1.3 * s - 0.7 * s, cy, cz - 2.2 * s, cx + sx * 1.3 * s + 0.7 * s, cy + 0.9 * s,
              cz - 0.4 * s, solid("foot"))                                    # pink feet
    rod(m, bone, (cx, cy + 9.6 * s, cz), (cx + 0.6 * s, cy + 11.4 * s, cz - 0.3 * s), 0.6 * s, solid("grey_dark"),
        extend=0.2)                                                          # the little curl of hair
    if tail:
        pts = [(cx, cy + 1 * s, cz + 1.8 * s), (cx + 2.4 * s, cy + 0.8 * s, cz + 1.2 * s),
               (cx + 3 * s, cy + 1.2 * s, cz - 1.6 * s), (cx + 1 * s, cy + 2.6 * s, cz - 3 * s)]
        for a, b, t in zip(pts, pts[1:], (1.4, 1.2, 1.0)):
            rod(m, bone, a, b, max(0.6, t * s), tailf, extend=0.3)
