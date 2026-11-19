"""Vajramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the ox general of the Twelve Devas: a bull-headed centaur with curved golden horns and a black muzzle,
a muscled black torso under red armour edged in gold, a black ox body with red-and-gold barding, cloven hooves, a
tufted tail, and a long straight sword in each hand. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 42
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a bull-headed centaur warrior with golden horns, red armour edged in gold, a black ox body and a long sword in each hand"
BASE = {"black": (44, 40, 46), "black_dark": (16, 14, 18), "red": (200, 40, 40), "red_dark": (120, 14, 14),
        "gold": (240, 196, 60), "gold_dark": (170, 120, 20), "steel": (220, 224, 234), "steel_dark": (120, 124, 140),
        "eye": (250, 220, 80), "tuft": (240, 220, 140)}
SHINY = {"red": (60, 110, 200), "red_dark": (20, 50, 120)}


def P(v):
    return pal(BASE, SHINY, v)


BLACK = skin(P, "black", dark="black_dark")
RED = armour(P, "red", "red_dark", trim="gold", panel=(3.0, 3.0))
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("vajramon")
    top = m.bone("vajramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(6):                                                                 # ox body
        z0 = -10.0 + i * 3.6
        slab_z(m, bd, 0, 16.0, z0, z0 + 3.8, 5.2, 5.0, RED if i in (0, 1) else BLACK)
    for sx, sz, nm in ((1, -8.0, "leg_front_left"), (-1, -8.0, "leg_front_right"), (1, 8.0, "leg_back_left"),
                       (-1, 8.0, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 3.4, 13.0, sz))
        rod(m, lg, (sx * 3.4, 13.0, sz), (sx * 3.6, 6.0, sz - 0.6), 2, RED, extend=0.4)
        rod(m, lg, (sx * 3.6, 6.0, sz - 0.6), (sx * 3.6, 1.6, sz), 2, BLACK, extend=0.4)
        m.round_box(lg, sx * 3.6, sz - 0.4, 1.6, 1.8, 0.0, 1.8, solid(P, "black_dark"), cut=0)
    tor = m.bone("torso", bd, (0, 20, -9))                                             # centaur torso
    m.round_box(tor, 0, -9.0, 4.4, 3.4, 20.0, 30.0, BLACK, cut=1)
    m.round_box(tor, 0, -9.4, 5.0, 3.8, 24.0, 31.0, RED, cut=1)
    for sx in (-1, 1):
        m.round_box(tor, sx * 6.4, -9.0, 2.6, 2.8, 28.0, 32.4, RED, cut=1)
        spike(m, tor, (sx * 7.4, 32.0, -9.0), (sx * 0.5, 1, 0), 1.2, 3.0, GOLD, tip=0.8)
    m.round_box(tor, 0, -9.0, 5.2, 3.6, 20.0, 21.4, GOLD, cut=1)
    hd = m.bone("head", tor, (0, 32, -9))
    m.round_box(hd, 0, -10.0, 2.8, 3.4, 32.0, 38.0, BLACK, cut=1)
    m.round_box(hd, 0, -13.0, 2.0, 1.4, 32.4, 35.0, solid(P, "black_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 35.8, -13.5, max(sx * 0.8, sx * 2.2), 36.6, -13.2, solid(P, "eye", glow=True))
        pts = [(sx * 2.6, 37.0, -10.0), (sx * 6.0, 38.0, -10.0), (sx * 7.0, 41.0, -10.6), (sx * 5.6, 43.0, -11.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 if i < 1 else 1, GOLD, extend=0.3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # arms + swords
        ab = m.bone(nm, tor, (sx * 6.0, 30.0, -9.0))
        rod(m, ab, (sx * 6.0, 30.0, -9.0), (sx * 9.0, 24.0, -11.0), 2, BLACK, extend=0.4)
        rod(m, ab, (sx * 9.0, 24.0, -11.0), (sx * 11.0, 20.0, -14.0), 2, RED, extend=0.4)
        m.box(ab, sx * 11.0 - 1.6, 19.4, -14.6, sx * 11.0 + 1.6, 20.4, -13.4, GOLD)
        m.box(ab, sx * 11.0 - 0.4, 20.0, -14.4, sx * 11.0 + 0.4, 21.0, -13.6, solid(P, "black"))
        x0, x1 = sorted((sx * 11.0, sx * 32.0))
        m.box(ab, x0, 19.6, -14.4, x1, 20.4, -13.6, metal(P, "steel", dark="steel_dark"),
              rotation=(0, 0, sx * -25), pivot=(sx * 11.0, 20.0, -14.0))
    tl = m.bone("tail", bd, (0, 18, 11))
    rod(m, tl, (0, 18.0, 11.0), (0, 10.0, 14.0), 1, BLACK, extend=0.3)
    ball(m, tl, (0, 9.0, 14.4), 1.2, strands(P, "tuft", "gold"), layers=1)
    return m
