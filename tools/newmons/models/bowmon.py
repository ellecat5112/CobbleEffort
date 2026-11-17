"""Bowmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a round blue puppy. A plump blue body with a big white muzzle and chest, floppy ears, a black nose,
red eyes under tan brow spots, a contented smile, four stubby legs and a fluffy blue-and-white tail. Baby II.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fur
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(0.5, HEIGHT, 0.55)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = ("a plump blue puppy with a big white muzzle and chest, floppy ears, red eyes under tan brow spots and a "
        "fluffy tail")
BASE = {"blue": (40, 70, 190), "blue_dark": (16, 30, 110), "blue_tip": (110, 140, 240), "white": (248, 248, 252),
        "white_dark": (190, 196, 214), "nose": (60, 40, 40), "eye": (220, 30, 50), "pupil": (30, 10, 10),
        "tan": (220, 170, 110), "line": (30, 20, 30)}
SHINY = {"blue": (200, 140, 60), "blue_dark": (130, 80, 20), "blue_tip": (250, 210, 140), "eye": (40, 150, 230)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "blue", "blue_dark", tip="blue_tip", length=1.1)
WHITE = fur(P, "white", "white_dark", length=1.0)


def bodyf(x, y, z, face, variant, box=None, **k):
    """Blue fur; the face: eyes with tan brow spots, a white muzzle and chest with a smile line."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 3.6, y - 14.0, 1.4, "eye")
            if c is not None:
                return c, None
            if abs(x - sx * 3.0) < 0.9 and abs(y - 16.4) < 0.4:
                return tone(p["tan"], face), None
        if y < 12.2 and abs(x) < 7.0 - max(0.0, y - 9.0):
            if abs(y - 8.8 - 0.08 * x * x) < 0.18 and abs(x) < 3.0:
                return tone(p["line"], face), None
            return WHITE(x, y, z, face, variant, box=box, **k)
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bowmon")
    top = m.bone("bowmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    ball(m, bd, (0, 12.0, 0), 9.0, bodyf, layers=7)
    m.box(bd, -2.4, 9.4, -9.8, 2.4, 12.6, -7.0, WHITE)                                # muzzle
    m.box(bd, -1.2, 11.4, -10.2, 1.2, 12.8, -9.6, fur(P, "nose", "nose", length=0.6))
    hd = m.bone("head", bd, (0, 18, 0))
    for sx in (-1, 1):                                                                # floppy ears
        m.box(hd, min(sx * 5.0, sx * 11.0), 16.0, -2.4, max(sx * 5.0, sx * 11.0), 17.6, 3.0, FUR,
              rotation=(0, 0, -sx * 30), pivot=(sx * 5.0, 17.6, 0))
    for fz, nm in ((-4.0, "front"), (4.0, "back")):                                  # four stubby legs
        for sx in (-1, 1):
            lg = m.bone(f"leg_{nm}_{'left' if sx > 0 else 'right'}", top, (sx * 4.4, 4.0, fz))
            m.round_box(lg, sx * 4.4, fz, 1.8, 1.8, 0.0, 5.0, FUR, cut=1)
    tl = m.bone("tail", bd, (0, 12, 8))
    rod(m, tl, (0, 12, 8), (3.0, 15.0, 12.0), 3, FUR, extend=0.4)
    rod(m, tl, (3.0, 15.0, 12.0), (5.0, 16.0, 13.4), 3, WHITE, extend=0.3)
    return m
