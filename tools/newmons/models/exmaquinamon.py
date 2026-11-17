"""Ex Maquinamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the god from the machine. A slender winged figure at the heart of a vast spread of wings: on one side layered golden
feathers, on the other white-and-silver blade feathers studded with glowing green lenses in gold rings, a rainbow halo
floating above, a crimson-and-violet body split down the middle, and a long chain of twisted cables hanging beneath.
35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, feathers, gem, metal, solid, twisted
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a slender figure in a vast spread of wings, golden feathers on one side and silver blade feathers with green "
        "lenses on the other, a rainbow halo and a long chain of twisted cables below")
BASE = {"gold": (250, 210, 80), "gold_dark": (180, 130, 30), "silver": (220, 224, 236), "silver_dark": (110, 114, 128),
        "green": (60, 220, 120), "green_light": (200, 255, 220), "crimson": (190, 30, 60), "violet": (90, 60, 150),
        "cable": (120, 80, 140), "cable_dark": (50, 30, 70), "r0": (250, 120, 160, 200), "r1": (250, 230, 120, 200),
        "r2": (120, 230, 170, 200), "r3": (120, 170, 250, 200), "white": (246, 246, 250)}
SHINY = {"gold": (230, 230, 240), "gold_dark": (140, 140, 160), "crimson": (40, 90, 200), "green": (230, 80, 160)}


def P(v):
    return pal(BASE, SHINY, v)


GOLDF = feathers(P, "gold", "gold_dark", size=(1.4, 3.0))
SILVER = metal(P, "silver", dark="silver_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("exmaquinamon")
    top = m.bone("exmaquinamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    for sx, key in ((-1, "crimson"), (1, "violet")):                                # body split down the middle
        x0, x1 = sorted((0.0, sx * 2.4))
        m.box(bd, x0, 24.0, -1.6, x1, 38.0, 1.6, armour(P, key, key, trim="gold", trim_w=0.3))
    hd = m.bone("head", bd, (0, 39, 0))
    m.round_box(hd, 0, 0, 1.6, 1.6, 38.0, 42.0, SILVER, cut=0)
    rb = m.bone("ring_halo", hd, (0, 46, 0))                                        # rainbow halo
    for i in range(16):
        a0, a1 = 2 * math.pi * i / 16, 2 * math.pi * (i + 1) / 16
        rod(m, rb, (4.0 * math.cos(a0), 46.0, 4.0 * math.sin(a0)), (4.0 * math.cos(a1), 46.0, 4.0 * math.sin(a1)), 1,
            solid(P, "r%d" % (i % 4), glow=True), extend=0.3)
    for row in range(3):                                                            # golden feather wing (left)
        wb = m.bone("wing_right_%d" % row, bd, (-2, 34, 1))
        for j in range(6):
            ang = math.radians(150 + j * 9 - row * 22)
            L = 24.0 - row * 4.0 - abs(j - 2.5)
            spike(m, wb, (-2.0, 34.0 - row * 2.0, 1.0 + row * 0.6), (math.cos(ang), math.sin(ang), 0.3), 2.4, L, GOLDF,
                  tip=0.8)
    for row in range(3):                                                            # silver blade wing (right)
        wb = m.bone("wing_left_%d" % row, bd, (2, 34, 1))
        for j in range(6):
            ang = math.radians(30 - j * 9 + row * 22)
            L = 26.0 - row * 4.0 - abs(j - 2.5)
            d = (math.cos(ang), math.sin(ang), 0.3)
            spike(m, wb, (2.0, 34.0 - row * 2.0, 1.0 + row * 0.6), d, 2.0, L, SILVER, tip=0.6)
            if j % 2 == 0:                                                          # green lenses in gold rings
                c = (2.0 + d[0] * L * 0.6, 34.0 - row * 2.0 + d[1] * L * 0.6, 0.0)
                m.round_box(wb, c[0], c[2], 1.6, 0.6, c[1] - 1.6, c[1] + 1.6, GOLD, cut=0)
                m.round_box(wb, c[0], c[2] - 0.4, 1.0, 0.4, c[1] - 1.0, c[1] + 1.0, gem(P, "green", "green_light"), cut=0)
    pts = [(0, 24.0, 0)]                                                            # twisted cable chain below
    for j in range(1, 7):
        pts.append((math.sin(j * 1.3) * 1.4, 24.0 - j * 3.6, math.cos(j * 1.3) * 0.8))
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 2, twisted(P, "cable", "cable_dark"), extend=0.5)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):
        m.bone(nm, bd, (sx * 2.4, 36.0, 0))
    return m
