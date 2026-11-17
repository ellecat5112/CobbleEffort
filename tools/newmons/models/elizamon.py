"""Elizamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
frilled lizard pup. A crouching magenta lizard with sky-blue diamond markings, a big round head with large violet
eyes, a huge cyan frill fanned out round its face and a cyan bow-like ruff at its throat, cyan fins down its long tail
and pale claws. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fabric, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("a crouching magenta lizard with sky-blue diamonds, big violet eyes, a huge cyan face frill, a cyan throat ruff "
        "and cyan tail fins")
BASE = {"magenta": (220, 30, 110), "magenta_dark": (130, 10, 60), "magenta_light": (255, 120, 180), "cyan": (110, 220, 240),
        "cyan_dark": (40, 140, 180), "eye": (90, 70, 200), "pupil": (20, 16, 40), "claw": (250, 230, 240),
        "mouth": (120, 20, 50), "tooth": (250, 250, 246)}
SHINY = {"magenta": (240, 150, 40), "magenta_dark": (160, 80, 10), "magenta_light": (255, 210, 130)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "magenta", dark="magenta_dark", light="magenta_light", var=0.03)


def diamondf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "up", "north") and abs((x * 0.5) % 4.0 - 2.0) + abs((y * 0.5 + z * 0.3) % 4.0 - 2.0) < 0.7:
        return tone(p["cyan"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("elizamon")
    mats = {"skin": diamondf, "belly": SKIN, "neck": SKIN, "head": diamondf, "snout": SKIN, "jaw": SKIN,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": diamondf, "leg_lower": SKIN,
            "paw": SKIN, "claw": solid(P, "claw"), "tail": SKIN}
    a = quadruped(m, mats, "elizamon", length=14.0, body_y=7.0, body_rx=3.4, body_ry=3.4, chest_bulk=1.2,
                  neck=((0, 9, -6), (0, 12, -8)), head_len=7.0, head_w=4.4, head_h=4.4, snout=0.3, mouth_open=4,
                  teeth=0, leg_bulk=1.1, toes=3,
                  tail=((0, 7, 7), (2, 8, 12), (5, 10, 15), (8, 13, 16)), tail_r=(1.6, 1.2, 0.9, 0.7))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):                                                               # big violet eyes
        m.box(hd, min(sx * (ex - 1.0), sx * (ex + 0.2)), ey - 1.0, ez - 1.6, max(sx * (ex - 1.0), sx * (ex + 0.2)),
              ey + 1.0, ez + 0.2, solid(P, "eye"))
        m.box(hd, min(sx * (ex - 0.6), sx * (ex + 0.3)), ey - 0.5, ez - 1.7, max(sx * (ex - 0.6), sx * (ex + 0.3)),
              ey + 0.5, ez - 0.4, solid(P, "pupil"))
    fb = m.bone("frill", hd, (0, ey, ez + 2))                                        # huge cyan face frill
    for i in range(9):
        ang = math.radians(-20 + i * 27.5)
        m.box(fb, -2.0, ey, ez + 2.6, 2.0, ey + 6.0, ez + 2.6, fabric(P, "cyan", "cyan_dark"),
              rotation=(0, 0, math.degrees(ang) - 90), pivot=(0, ey, ez + 2.6))
    for sx in (-1, 1):                                                               # throat ruff bow
        m.box(bd, min(sx * 0.4, sx * 3.0), 8.0, -9.0, max(sx * 0.4, sx * 3.0), 10.4, -8.4, fabric(P, "cyan", "cyan_dark"),
              rotation=(0, 0, sx * 15), pivot=(0, 9.2, -8.7))
    for p in a["tail_pts"][1:]:                                                      # cyan tail fins
        spike(m, a["tail"], p, (0, 1, 0.3), 1.4, 2.0, solid(P, "cyan"), tip=0.4)
    return m
