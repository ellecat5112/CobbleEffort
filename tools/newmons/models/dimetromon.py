"""Dimetromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the sail-backed reptile. A sturdy four-legged magenta reptile covered in overlapping scales, with a
great translucent sky-blue sail of folded ribs rising along its back and down its tail, a ruffled white frill at its
throat, blue claws with white cuffs and a blunt, friendly snout. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fabric, local, scales, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a sturdy magenta scaled reptile with a great translucent sky-blue folded sail along its back and tail, a ruffled "
        "white throat frill and blue claws")
BASE = {"magenta": (190, 40, 110), "magenta_dark": (100, 14, 54), "magenta_light": (240, 120, 180),
        "sail": (120, 190, 250, 190), "sail_light": (220, 240, 255, 210), "white": (246, 248, 252),
        "white_dark": (190, 200, 216), "claw": (60, 110, 200), "eye": (40, 60, 160), "mouth": (130, 30, 60),
        "tooth": (250, 250, 246)}
SHINY = {"magenta": (90, 160, 80), "magenta_dark": (30, 80, 30), "magenta_light": (160, 220, 140),
         "sail": (250, 190, 90, 190)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "magenta", "magenta_dark", size=1.6, light="magenta_light", rim_mix=0.3)


def sailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["sail_light"] if v / max(H, 1e-6) > 0.85 or (u % 3.0) < 0.5 else p["sail"]
    return c, None


def build():
    m = Model("dimetromon")
    mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": HIDE, "leg_lower": HIDE, "paw": HIDE,
            "claw": solid(P, "claw"), "tail": HIDE}
    a = quadruped(m, mats, "dimetromon", length=30.0, body_y=12.0, body_rx=6.6, body_ry=6.0, chest_bulk=1.1,
                  neck=((0, 14, -14), (0, 17, -17)), head_len=8.0, head_w=3.6, head_h=3.8, snout=0.5, mouth_open=8,
                  teeth=0, leg_bulk=1.6, toes=3,
                  tail=((0, 12, 15), (0, 10, 21), (0, 9, 27), (0, 10, 33)), tail_r=(2.6, 2.0, 1.4, 1.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.5, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.5, ez + 0.6,
              solid(P, "eye"))
    for i in range(8):                                                       # ruffled white frill
        ang = math.radians(-90 + i * 26)
        m.box(bd, 3.0 * math.sin(ang) - 0.8, 10.0, -17.0 - 2.0 * math.cos(ang), 3.0 * math.sin(ang) + 0.8, 14.0,
              -16.4 - 2.0 * math.cos(ang), fabric(P, "white", "white_dark"), rotation=(20, 0, 0),
              pivot=(0, 14.0, -16.5))
    for i in range(11):                                                      # the folded sail
        t = i / 10
        z = -10.0 + 36.0 * t
        h = 16.0 * math.sin(math.pi * min(1.0, t * 1.15)) + 2.0
        y0 = 17.0 - 6.0 * max(0.0, t - 0.6)
        m.box(bd, -0.2, y0, z, 0.2, y0 + h, z + 3.6, sailf, rotation=(0, (-1) ** i * 18, 0), pivot=(0, y0, z + 1.8))
        rod(m, bd, (0, y0, z), (0, y0 + h, z + 0.4), 1, solid(P, "sail_light"), extend=0)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 2.6, 2.6, 4.0, 5.4, fabric(P, "white", "white_dark"), cut=1)
    return m
