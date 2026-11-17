"""Deadly Axemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the living battle-axe. A lunging black demon beast of glossy round armour segments trimmed in
gold, its head a gold-crested mask with red fangs and swept gold horns, arms ending in long curved gold axe-blades,
legs that taper to gold drill points, and a spray of gold spikes along its back and tail. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lunging black demon beast of glossy armour segments trimmed in gold, a gold-crested fanged mask, curved "
        "axe-blade arms and drill-pointed legs")
BASE = {"black": (44, 44, 52), "black_dark": (12, 12, 16), "black_light": (140, 140, 160), "gold": (240, 196, 60),
        "gold_dark": (160, 110, 20), "red": (200, 30, 40), "eye": (250, 220, 60), "tooth": (250, 248, 240)}
SHINY = {"black": (230, 230, 236), "black_dark": (150, 150, 160), "black_light": (255, 255, 255),
         "gold": (90, 200, 240), "gold_dark": (30, 110, 170)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")


def segs(m, bone, a, b, n, r0, r1):
    """Glossy round armour segments from a to b."""
    for j in range(n):
        t = (j + 0.5) / n
        c = tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
        r = r0 + (r1 - r0) * t
        m.round_box(bone, c[0], c[2], r, r, c[1] - r * 0.9, c[1] + r * 0.9, SHELL, cut=max(1, round(r * 0.4)))


def build():
    m = Model("deadlyaxemon")
    top = m.bone("deadlyaxemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    segs(m, bd, (0, 18.0, 6.0), (0, 26.0, -4.0), 4, 5.0, 4.2)                        # lunging torso
    hd = m.bone("head", bd, (0, 28, -6))
    m.round_box(hd, 0, -8.0, 3.0, 3.6, 26.0, 31.0, SHELL, cut=1)                       # mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.6), 29.0, -11.8, max(sx * 1.0, sx * 2.6), 29.8, -11.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.4, 30.6, -7.0), (sx * 0.6, 0.6, 1), 1.6, 9.0, GOLD, tip=0.2)    # swept horns
        spike(m, hd, (sx * 1.6, 26.4, -11.0), (0, -1, -0.2), 0.8, 2.4, solid(P, "red"), tip=0.25)   # red fangs
    spike(m, hd, (0, 31.0, -9.0), (0, 1, 0.6), 1.4, 6.0, GOLD, tip=0.2)                # gold crest
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.6, 26.0, -2.0))
        segs(m, ab, (sx * 4.6, 26.0, -2.0), (sx * 10.0, 22.0, -10.0), 3, 2.8, 2.2)
        blade = [(sx * 10.0, 22.0, -10.0), (sx * 12.0, 18.0, -15.0), (sx * 12.0, 13.0, -17.0), (sx * 10.0, 9.0, -16.0)]
        for p0, p1 in zip(blade, blade[1:]):                                          # curved axe-blade
            rod(m, ab, p0, p1, 1, GOLD, extend=0.5, t2=4)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 18.0, 4.0))
        segs(m, lg, (sx * 4.0, 18.0, 4.0), (sx * 6.0, 6.0, 2.0), 3, 3.2, 2.4)
        spike(m, lg, (sx * 6.0, 4.4, 2.0), (0, -1, 0), 3.4, 4.4, GOLD, tip=0.2)         # drill point
    tl = m.bone("tail", bd, (0, 18, 8))
    segs(m, tl, (0, 18.0, 8.0), (4.0, 22.0, 18.0), 3, 3.0, 1.6)
    for i in range(10):                                                                # back + tail spikes
        t = i / 9
        p = (4.0 * t, 22.0 + 4.0 * (1 - t), -2.0 + 20.0 * t)
        spike(m, bd if i < 5 else tl, p, (0.2, 1, 0.4), 1.4, 4.0 - 1.4 * t, GOLD, tip=0.2)
    return m
