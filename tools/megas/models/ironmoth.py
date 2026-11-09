"""Mega Iron Moth, hand-built from boxes in Cobblemon's style.

Iron Moth (official art: a future Volcarona robot: six orange triangular wing panels arranged round it like a sun,
each with a dark triangle mark and sparkles; a white mask-like face with black markings and red horns; a pale
blue-white body with a black lower shell) as a mega: eight panels in a full blazing halo, glowing at their tips, and
a crest of red horns.

Front is -z, y is up. ~40 units tall; baseScale 1.0 (about 2.5 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.0
HITBOX = [2.4, 2.5]
LOOK = ("a robot Volcarona in a halo of eight glowing orange wing panels with dark triangle marks, a white mask face "
        "with black markings, a crest of red horns and a pale body with a black shell")
KIND = "floater"
ANIM = {"wing_flap": 4}

BASE = {"orange": (250, 150, 50), "orange_light": (255, 196, 100), "mark": (60, 40, 30), "white": (244, 244, 248),
        "pale": (200, 220, 236), "black": (34, 34, 44), "red": (220, 50, 40), "eye": (60, 200, 255)}
SHINY = {"orange": (120, 200, 250), "orange_light": (180, 230, 255), "red": (250, 160, 40), "eye": (255, 110, 160)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def panel(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, **k):
    """A wing panel: a triangle (cut out beyond its sides), orange with a dark triangle mark, glowing at the tip."""
    P = palette(variant)
    t = r / max(1, rows - 1)                           # 0 at the outer tip, 1 at the root
    half = (cols - 1) / 2
    if abs(c - half) > half * (0.15 + 0.85 * (1 - abs(t - 0.45) / 0.55)):
        return (0, 0, 0, 0)
    if t < 0.18:
        return P["orange_light"], P["orange_light"]
    if 0.45 < t < 0.75 and abs(c - half) < half * 0.35 * (t - 0.4) * 3:
        return P["mark"]
    return P["orange"]


def facef(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north":
        if 23 <= y <= 25 and 1 <= abs(x) <= 3:
            return P["eye"], P["eye"]
        if (abs(x) < 0.6 and y > 21) or (20 <= y <= 21 and abs(x) < 3):
            return P["black"]                          # mask markings
        return P["white"]
    return P["white"]


def bodyf(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["black"] if y < 14 else P["pale"]


def red(x, y, z, face, variant, **k):
    return palette(variant)["red"]


def build() -> Model:
    m = Model("ironmoth_mega")
    root = m.bone("ironmoth_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 18, 0))
    m.round_box(body, 0, 0, 4, 4, 8, 20, bodyf, cut=1)
    hd = m.bone("head", body, (0, 20, 0))
    m.round_box(hd, 0, 0, 4, 3, 19, 28, facef, cut=1)
    for sgn in (1, -1):
        chain(m, hd, [(sgn * 2.5, 27.5, -1), (sgn * 5, 31, 0), (sgn * 5, 34, 2)], [2, 1.5], red)
    # the halo: eight triangular panels round the body, split into a left and a right wing
    for sgn, side in ((1, "left"), (-1, "right")):
        wb = m.bone(f"wing_{side}", body, (0, 17, 2))
        for n in range(4):
            ang = sgn * (22.5 + 45 * n)                # degrees from straight up, round to straight down
            a = math.radians(ang)
            px, py = 5 * math.sin(a), 17 + 5 * math.cos(a)
            m.box(wb, px - 5, py, 3, px + 5, py + 16, 3, panel, rotation=(0, 0, ang), pivot=(px, py, 3))
    return m
