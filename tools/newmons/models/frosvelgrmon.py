"""Fros Velgrmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the frost raptor of Royal Knight legend. A tall white-and-silver bird of prey standing
on scaled blue legs with gold ankle rings and steel talons, a narrow crested head with a hooked beak and a crown of
ice-blue crystal plumes, a glowing ice orb above its brow, swept white-and-blue wings, and an enormous fan of
glowing icy-blue tail plumes streaming far behind. 35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digidetail import feathers, local, metal, scales, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall white-and-silver bird of prey on scaled blue legs with gold rings, a crested hooked-beak head with ice "
        "crystal plumes and a glowing ice orb, swept wings and an enormous fan of glowing icy tail plumes")
BASE = {"white": (240, 244, 250), "white_dark": (170, 180, 200), "silver": (190, 200, 216), "blue": (90, 110, 190),
        "blue_dark": (40, 50, 110), "ice": (120, 210, 255, 210), "ice_core": (220, 250, 255, 235), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "steel": (220, 224, 234), "steel_dark": (110, 114, 126), "beak": (60, 64, 90),
        "eye": (220, 30, 50), "red": (200, 30, 40)}
SHINY = {"ice": (255, 140, 200, 210), "ice_core": (255, 230, 245, 235), "blue": (150, 70, 160), "blue_dark": (80, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


PLUME = feathers(P, "white", "white_dark", tip="blue", size=(1.4, 2.4))
LEG = scales(P, "blue", "blue_dark", size=1.0)


def icef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["ice_core"] if abs(u - W / 2) < W * 0.15 or (u * 1.4 + v) % 2.4 < 0.4 else p["ice"]
    return c, c[:3]


def build():
    m = Model("frosvelgrmon")
    top = m.bone("frosvelgrmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    for j, (r, y0) in enumerate(((5.0, 22.0), (5.6, 27.0), (5.0, 32.0), (3.8, 37.0))):    # upright torso
        m.round_box(bd, 0, -1.0 - j * 0.6, r, r * 0.9, y0, y0 + 5.6, PLUME, cut=2)
    m.round_box(bd, 0, -5.4, 2.6, 0.8, 29.0, 33.0, solid(P, "red"), cut=0)              # red chest mark
    hd = m.bone("head", bd, (0, 42, -3))
    rod(m, bd, (0, 40.0, -3.0), (0, 45.0, -4.0), 3, PLUME, extend=0.4)                  # neck
    m.round_box(hd, 0, -4.4, 2.4, 3.6, 44.0, 49.6, PLUME, cut=1)
    spike(m, hd, (0, 46.0, -8.0), (0, -0.5, -1), 2.0, 4.0, solid(P, "beak"), tip=0.3)   # hooked beak
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.4, sx * 2.5), 47.4, -6.6, max(sx * 2.4, sx * 2.5), 48.2, -5.6, solid(P, "eye", glow=True))
    for i in range(7):                                                                  # ice crystal plumes
        ang = math.radians(-45 + i * 15)
        spike(m, hd, (2.0 * math.sin(ang), 49.0, -3.0), (math.sin(ang) * 0.8, 1.0, 0.6), 1.2, 8.0 - abs(i - 3), icef,
              tip=0.2)
    m.round_box(hd, 0, -6.0, 1.6, 1.6, 50.0, 53.2, icef, cut=1)                         # ice orb
    for side in (1, -1):                                                                # swept wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 38.0, 1.0))
        feather_wing(m, wb, (side * 5.0, 38.0, 1.0), 18.0, 8.0, 3, PLUME, side=side, sweep=40, droop=-4.0)
    tb = m.bone("tail", bd, (0, 24, 4))                                                 # enormous icy tail fan
    for i in range(9):
        ang = math.radians(-40 + i * 10)
        for j in range(3):
            y = 24.0 - 3.0 * j + 6.0 * math.sin(ang)
            z0 = 4.0 + j * 11.0
            m.box(tb, -1.6 + 9.0 * math.sin(ang) * (1 + j * 0.6), y, z0, 1.6 + 9.0 * math.sin(ang) * (1 + j * 0.6),
                  y + 0.6, z0 + 12.0, icef)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                 # scaled legs, talons
        lg = m.bone(nm, top, (sx * 3.0, 22.0, 0))
        rod(m, lg, (sx * 3.0, 23.0, 0), (sx * 3.4, 12.0, 1.0), 2, PLUME, extend=0.4)
        rod(m, lg, (sx * 3.4, 12.0, 1.0), (sx * 3.4, 2.0, -1.0), 1, LEG, extend=0.3, t2=1)
        m.round_box(lg, sx * 3.4, 0.4, 1.4, 1.4, 6.0, 7.2, metal(P, "gold", dark="gold_dark"), cut=0)
        for j in range(3):
            spike(m, lg, (sx * 3.4 + (j - 1) * 1.2, 1.0, -1.6), ((j - 1) * 0.4, -0.3, -1), 0.8, 3.6,
                  metal(P, "steel", dark="steel_dark"), tip=0.2)
        spike(m, lg, (sx * 3.4, 1.0, 0.4), (0, -0.3, 1), 0.8, 2.4, metal(P, "steel", dark="steel_dark"), tip=0.2)
    return m
