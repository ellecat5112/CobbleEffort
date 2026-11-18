"""Mastemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the angel-demon of judgement: a slender figure in white-and-black segmented armour with a gold halo
and long pale hair, white feathered angel wings on one side and black tattered demon wings on the other, and twin
rings of red and blue light spiralling round its feet. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, feather_wing
from _digibody import humanoid
from _digidetail import armour, cutout, feathers, local, noise2, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a slender figure in white-and-black armour with a gold halo, white angel wings on one side and black demon wings on the other"
BASE = {"white": (246, 246, 250), "white_dark": (180, 182, 200), "black": (36, 34, 40), "black_dark": (10, 10, 12),
        "gold": (240, 200, 70), "red": (240, 80, 100), "blue": (90, 160, 250), "hair": (240, 236, 220),
        "hair_dark": (190, 180, 160), "eye": (220, 40, 60)}
SHINY = {"gold": (200, 220, 255), "red": (255, 180, 60), "blue": (180, 90, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def armf(x, y, z, face, variant, box=None, **k):
    if x < 0:
        return armour(P, "black", "black_dark", trim="gold", trim_w=0.2)(x, y, z, face, variant, box=box, **k)
    return armour(P, "white", "white_dark", trim="gold", trim_w=0.2)(x, y, z, face, variant, box=box, **k)


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.14 * abs(math.sin(u * 0.8)) + 0.06 * noise2(u, 0.0, 9)


def build():
    m = Model("mastemon")
    mats = {k: armf for k in ("skin", "chest", "abs", "pelvis", "neck", "deltoid", "upper_arm", "forearm", "hand", "finger",
                              "thigh", "knee", "shin", "calf", "foot", "toe")}
    a = humanoid(m, mats, bulk=0.75, arm_bulk=0.75, leg_bulk=0.8, name="mastemon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.2, 2.6, 54.0, 60.0, armf, cut=1)
    m.box(hd, -1.4, 57.2, -2.9, 1.4, 57.8, -2.8, solid(P, "eye", glow=True))
    for i in range(9):
        ang = math.radians(-100 + i * 25)
        rod(m, hd, (2.0 * math.sin(ang), 59.6, 0.8 + 1.2 * math.cos(ang)), (3.0 * math.sin(ang), 46.0, 3.0), 1,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    hb = m.bone("ring_halo", hd, (0, 63, 1))
    for i in range(12):
        a0, a1 = 2 * math.pi * i / 12, 2 * math.pi * (i + 1) / 12
        rod(m, hb, (3.4 * math.cos(a0), 63.0, 1.0 + 3.4 * math.sin(a0)), (3.4 * math.cos(a1), 63.0, 1.0 + 3.4 * math.sin(a1)),
            1, solid(P, "gold", glow=True), extend=0.2, t2=1)
    wl = m.bone("wing_left", bd, (2.6, 50.0, 3.4))                                   # white angel wings
    for j, dr in enumerate((18, 0, -18)):
        feather_wing(m, wl, (2.6, 50.0, 3.4 + j * 0.4), 26.0, 8.0, 2, feathers(P, "white", "white_dark"), side=1, sweep=15, droop=dr)
    wr = m.bone("wing_right", bd, (-2.6, 50.0, 3.4))                                 # black demon wings
    for j, sw in enumerate((10, 35)):
        bat_wing(m, wr, (-2.6, 50.0 - j * 6.0, 3.4 + j * 0.4), 26.0, 18.0, 4, solid(P, "black"),
                 cutout(tatter, solid(P, "black_dark")), side=-1, sweep=sw)
    rb = m.bone("ring_light", bd, (0, 6, 0))                                          # spiralling light rings
    for k_, (key, r, y0) in enumerate((("red", 9.0, 6.0), ("blue", 11.0, 2.0))):
        for i in range(14):
            a0, a1 = 2 * math.pi * i / 14, 2 * math.pi * (i + 1) / 14
            rod(m, rb, (r * math.cos(a0), y0 + i * 0.3, r * math.sin(a0)), (r * math.cos(a1), y0 + (i + 1) * 0.3, r * math.sin(a1)),
                1, solid(P, key, glow=True), extend=0.2, t2=1)
    return m
