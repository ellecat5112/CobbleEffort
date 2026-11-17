"""Done Devimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the fallen angel of ruin. A hunched, gaunt black-and-silver demon with a pointed hooded head,
small red eyes and a sharp grin, curved blade-wings sweeping from its back like scythes, a long scythe-tipped tail,
skinny legs ending in red talons, and in place of arms two colossal floating grey stone hands, one clenched into a
fist and one pointing, trailing black ink-like spatters. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hunched gaunt black-and-silver demon with a pointed hood, scythe blade-wings, a scythe tail, red talons and two "
        "colossal floating stone hands, a fist and a pointing hand")
BASE = {"black": (44, 40, 54), "black_dark": (12, 10, 18), "black_light": (130, 120, 150), "silver": (200, 200, 214),
        "silver_dark": (100, 100, 116), "stone": (150, 150, 156), "stone_dark": (80, 80, 88), "stone_light": (210, 210, 216),
        "red": (210, 30, 40), "eye": (250, 40, 40), "ink": (20, 20, 26)}
SHINY = {"black": (230, 230, 236), "black_dark": (150, 150, 160), "stone": (190, 150, 110), "stone_dark": (110, 80, 50)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = armour(P, "black", "black_dark", light="black_light", trim="silver", trim_w=0.3)
STONE = skin(P, "stone", dark="stone_dark", light="stone_light", var=0.08)
SILVER = metal(P, "silver", dark="silver_dark")


def blade(m, bone, base, sx, length, rise):
    pts = [base]
    for j in range(1, 5):
        t = j / 4
        pts.append((base[0] + sx * length * t, base[1] + rise * math.sin(t * 2.4), base[2] + 6.0 * t))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bone, p0, p1, 1, SILVER if j % 2 else HIDE, extend=0.5, t2=max(1, 5 - j))


def hand(m, bone, c, sx, fist):
    m.round_box(bone, c[0], c[2], 6.0, 5.0, c[1] - 5.0, c[1] + 5.0, STONE, cut=2)          # colossal palm
    m.round_box(bone, c[0] - sx * 7.0, c[2] + 2.0, 2.4, 2.4, c[1] - 3.0, c[1] + 1.0, STONE, cut=1)  # thumb
    for j in range(4):
        x = c[0] + (j - 1.5) * 2.8
        if fist:
            m.round_box(bone, x, c[2] - 5.4, 1.4, 1.6, c[1] - 2.0, c[1] + 4.0, STONE, cut=0)
        elif j == 0:
            rod(m, bone, (x, c[1] + 2.0, c[2] - 4.0), (x - sx * 10.0, c[1] + 4.0, c[2] - 10.0), 3, STONE, extend=0.6)
        else:
            m.round_box(bone, x, c[2] - 5.0, 1.4, 1.6, c[1] - 2.0, c[1] + 3.0, STONE, cut=0)
    for i in range(6):                                                                     # ink spatters
        ang = i * 1.7
        m.round_box(bone, c[0] + 7.0 * math.cos(ang), c[2] + 6.0 + 2.0 * math.sin(ang), 0.8, 0.8,
                    c[1] - 8.0 + i * 2.6, c[1] - 7.0 + i * 2.6, solid(P, "ink"), cut=0)


def build():
    m = Model("donedevimon")
    top = m.bone("donedevimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    m.round_box(bd, 0, 1.0, 5.0, 4.0, 16.0, 30.0, HIDE, cut=2)                            # hunched body
    hd = m.bone("head", bd, (0, 30, -3))
    m.round_box(hd, 0, -3.0, 2.8, 3.2, 28.0, 34.0, HIDE, cut=1)
    spike(m, hd, (0, 33.0, -1.0), (0, 0.6, 1), 2.6, 7.0, HIDE, tip=0.6)                    # pointed hood
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 31.0, -6.3, max(sx * 0.6, sx * 1.8), 31.6, -6.1, solid(P, "eye", glow=True))
    m.box(hd, -1.6, 29.0, -6.3, 1.6, 29.4, -6.1, solid(P, "silver"))                      # sharp grin
    for sx in (-1, 1):                                                                     # scythe blade-wings
        blade(m, bd, (sx * 3.0, 28.0, 3.0), sx, 26.0, 10.0)
        blade(m, bd, (sx * 3.0, 24.0, 3.0), sx, 20.0, -6.0)
    for sx, nm, fist in ((1, "arm_left", True), (-1, "arm_right", False)):                 # floating stone hands
        ab = m.bone(nm, bd, (sx * 6.0, 28.0, 0))
        hand(m, ab, (sx * 14.0, 44.0 if fist else 40.0, -6.0), sx, fist)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                    # skinny legs, red talons
        lg = m.bone(nm, top, (sx * 3.0, 18.0, 0))
        rod(m, lg, (sx * 3.0, 18.0, 0), (sx * 6.0, 10.0, -3.0), 2, HIDE, extend=0.4)
        rod(m, lg, (sx * 6.0, 10.0, -3.0), (sx * 6.0, 2.0, 1.0), 2, HIDE, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 6.0 + (j - 1) * 1.2, 1.0, 0.0), ((j - 1) * 0.3, -0.2, -1), 1.0, 4.0, solid(P, "red"),
                  tip=0.25)
    tl = m.bone("tail", bd, (0, 18, 4))
    pts = [(0, 18.0, 4.0), (4.0, 12.0, 12.0), (10.0, 8.0, 18.0), (18.0, 8.0, 20.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, HIDE, extend=0.5)
    blade(m, tl, (18.0, 8.0, 20.0), 1, 12.0, -6.0)                                         # scythe tail tip
    return m
