"""Jazardmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Jazamon grown into a machine dragon: a hunched navy-and-silver mecha dragon with a sharp visored
head, red eyes and a cyan face light, swept blade fins, a ribbed silver chest, two great disc turbines on its
shoulders blazing with blue jet fire, swept cyan-edged wings and long legs ending in blade talons. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, cutout, flame_inside, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hunched navy-and-silver mecha dragon with a visored head, red eyes, two great disc turbines blazing blue jet "
        "fire, cyan-edged swept wings and blade talons")
BASE = {"navy": (40, 50, 130), "navy_dark": (14, 18, 60), "navy_light": (110, 120, 210), "silver": (210, 214, 226),
        "silver_dark": (100, 104, 120), "cyan": (90, 230, 250), "cyan_light": (220, 255, 255), "eye": (240, 40, 40),
        "black": (24, 24, 34), "jet": (120, 200, 255, 210), "jet_core": (235, 250, 255, 240)}
SHINY = {"navy": (140, 30, 40), "navy_dark": (70, 10, 14), "navy_light": (220, 110, 110)}


def P(v):
    return pal(BASE, SHINY, v)


NAVY = armour(P, "navy", "navy_dark", light="navy_light", trim="cyan", trim_w=0.2)
SILVER = metal(P, "silver", dark="silver_dark")
LIGHT = gem(P, "cyan", "cyan_light")


def jetf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["jet_core"] if v / max(H, 1e-6) < 0.3 else p["jet"]
    return c, c[:3]


def discf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        u, v, W, H = local(x, y, z, face, box)
        r = math.hypot(u - W / 2, v - H / 2)
        if r < 1.2:
            return tone(p["cyan_light"], face), p["cyan"]
        if abs(r - W * 0.35) < 0.3:
            return tone(p["silver_dark"], face), None
    return SILVER(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("jazardmon")
    top = m.bone("jazardmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    m.round_box(bd, 0, 0.0, 5.0, 5.0, 17.0, 29.0, NAVY, cut=2)
    for j in range(4):
        m.round_box(bd, 0, -5.0, 3.6 - j * 0.4, 0.5, 19.0 + j * 2.4, 20.4 + j * 2.4, SILVER, cut=0)  # ribbed chest
    hd = m.bone("head", bd, (0, 29, -4))
    m.round_box(hd, 0, -6.0, 2.8, 4.6, 28.0, 33.4, NAVY, cut=1)
    spike(m, hd, (0, 30.0, -10.4), (0, -0.3, -1), 2.0, 4.0, NAVY, tip=0.8)
    m.round_box(hd, 0, -10.2, 0.8, 0.4, 30.6, 32.0, LIGHT, cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.4, sx * 2.9), 31.4, -9.0, max(sx * 2.4, sx * 2.9), 32.4, -7.0, solid(P, "eye", glow=True))
        for j in range(2):
            spike(m, hd, (sx * 2.0, 32.6 - j * 1.6, -5.0 + j * 2.0), (sx * 0.5, 0.6, 1), 1.4, 6.0 - j, NAVY, tip=0.8)
    for sx in (-1, 1):                                                               # disc turbines
        m.box(bd, min(sx * 6.0, sx * 9.0), 20.0, -4.0, max(sx * 6.0, sx * 9.0), 30.0, 6.0, discf)
        for ang in (0, 90):
            m.box(bd, sx * 7.5 - 2.6, 13.0, 1.0, sx * 7.5 + 2.6, 20.0, 1.0, cutout(flame_inside(4, 0.0, 2, 0.3), jetf),
                  rotation=(180, ang, 0), pivot=(sx * 7.5, 20.0, 1.0))
    for side in (1, -1):                                                             # swept wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 28.0, 4.0))
        rod(m, wb, (side * 4.0, 28.0, 4.0), (side * 12.0, 36.0, 10.0), 2, NAVY, extend=0.4)
        rod(m, wb, (side * 12.0, 36.0, 10.0), (side * 20.0, 38.0, 14.0), 1, NAVY, extend=0.4, t2=3)
        m.round_box(wb, side * 20.0, 14.0, 1.0, 1.6, 36.6, 39.4, LIGHT, cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 24.0, -3.0))
        rod(m, ab, (sx * 4.0, 24.0, -3.0), (sx * 5.0, 16.0, -6.0), 1, SILVER, extend=0.3, t2=2)
        for j in range(3):
            spike(m, ab, (sx * 5.0 + (j - 1) * 0.8, 15.4, -6.4), (0, -1, -0.4), 0.9, 3.0, solid(P, "cyan"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 18.0, 0))
        rod(m, lg, (sx * 3.0, 18.0, 0), (sx * 4.0, 10.0, 3.0), 3, NAVY, extend=0.6)
        rod(m, lg, (sx * 4.0, 10.0, 3.0), (sx * 4.0, 2.0, 0), 2, SILVER, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 4.0 + (j - 1) * 1.2, 1.0, -1.0), ((j - 1) * 0.3, -0.2, -1), 1.0, 5.0, NAVY, tip=0.8)
    rod(m, bd, (0, 18.0, 4.0), (0, 12.0, 14.0), 2, NAVY, extend=0.4, t2=1)
    return m
