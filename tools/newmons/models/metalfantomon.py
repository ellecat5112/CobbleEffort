"""Metal Fantomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the cyborg reaper: a skull face under a black armoured hood, a steel skeleton of ribs
and arms crackling with violet lightning, a sweeping crimson cloak in tatters, a red jewel at its chest, and a long
black scythe with a pink energy blade and a glowing pink orb hanging from its haft. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape
from _digidetail import armour, fabric, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = ("a cyborg reaper: a skull under a black armoured hood, a steel skeleton crackling with lightning, a tattered "
        "crimson cloak and a long black scythe with a pink energy blade and a glowing orb")
BASE = {"black": (36, 34, 42), "black_dark": (12, 12, 16), "bone": (230, 228, 222), "bone_dark": (150, 146, 140),
        "steel": (180, 186, 200), "steel_dark": (90, 96, 110), "red": (190, 20, 30), "red_dark": (100, 6, 12),
        "pink": (250, 120, 200, 200), "pink_core": (255, 220, 245, 230), "eye": (250, 60, 60),
        "bolt": (170, 160, 255)}
SHINY = {"red": (40, 60, 160), "red_dark": (14, 24, 90), "pink": (120, 230, 255, 200), "pink_core": (230, 250, 255, 230)}


def P(v):
    return pal(BASE, SHINY, v)


HOOD = armour(P, "black", "black_dark", trim="steel", trim_w=0.2)
STEEL = metal(P, "steel", dark="steel_dark")
CLOAK = fabric(P, "red", "red_dark")


def energyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["pink_core"] if v / max(H, 1e-6) > 0.6 else p["pink"]
    return c, c[:3]


def build():
    m = Model("metalfantomon")
    top = m.bone("metalfantomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    for j in range(8):                                                                   # flowing cloak body
        r = 4.0 + j * 1.2
        m.round_box(bd, 0, 1.0, r, r * 0.8, 46.0 - (j + 1) * 5.0, 46.4 - j * 5.0, CLOAK, cut=max(1, int(r * 0.3)))
    cape(m, bd, 50.0, 18.0, 44.0, CLOAK, z=4.0, flare=1.0, panels=6, seed=7)
    m.round_box(bd, 0, 0.0, 4.6, 3.0, 40.0, 50.0, STEEL, cut=1)                            # steel ribcage
    for j in range(4):
        m.box(bd, -4.8, 41.0 + j * 2.2, -3.4, 4.8, 42.0 + j * 2.2, -3.0, solid(P, "bone"))
    ball(m, bd, (0, 47.0, -3.6), 1.0, gem(P, "red", "pink_core"), layers=2)
    hd = m.bone("head", bd, (0, 54, 0))
    m.round_box(hd, 0, 0.0, 2.6, 2.8, 51.0, 57.0, armour(P, "bone", "bone_dark"), cut=1)   # skull
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 54.0, -2.9, max(sx * 0.6, sx * 1.8), 55.2, -2.8, solid(P, "black"))
        m.box(hd, min(sx * 0.9, sx * 1.4), 54.3, -2.95, max(sx * 0.9, sx * 1.4), 54.9, -2.9, solid(P, "eye", glow=True))
    for j in range(5):
        m.box(hd, -1.6 + j * 0.7, 51.6, -2.9, -1.2 + j * 0.7, 52.6, -2.8, solid(P, "black"))
    m.round_box(hd, 0, 1.0, 4.0, 4.0, 57.4, 59.8, HOOD, cut=1)                             # armoured hood: crown,
    m.round_box(hd, 0, 3.6, 4.0, 1.6, 50.0, 57.4, HOOD, cut=1)                             # back
    for sx in (-1, 1):                                                                     # and open sides
        x0, x1 = sorted((sx * 2.8, sx * 4.0))
        m.box(hd, x0, 50.0, -3.6, x1, 57.4, 2.0, HOOD)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                    # steel skeleton arms
        ab = m.bone(nm, bd, (sx * 5.0, 48.0, 0))
        rod(m, ab, (sx * 5.0, 48.0, 0), (sx * 10.0, 40.0, -4.0), 1, STEEL, extend=0.3, t2=1)
        rod(m, ab, (sx * 10.0, 40.0, -4.0), (sx * 9.0, 34.0, -9.0), 1, STEEL, extend=0.3, t2=1)
        for f in range(3):
            spike(m, ab, (sx * 9.0 + (f - 1) * 0.6, 34.0, -9.0), (0, -1, -0.5), 0.8, 2.6, STEEL, tip=0.8)
        for j in range(3):                                                                 # crackling lightning
            p0 = (sx * (7.0 + j), 44.0 - j * 3.0, -2.0 - j)
            rod(m, ab, p0, (p0[0] + sx * 2.0, p0[1] + 1.4, p0[2] - 1.0), 1, solid(P, "bolt", glow=True), extend=0.1)
    ar = "arm_right"                                                                       # the scythe
    rod(m, ar, (-14.0, 58.0, -7.0), (-4.0, 10.0, -11.0), 1, solid(P, "black"), extend=0.3, t2=1)
    m.box(ar, -16.0, 54.0, -7.5, -2.0, 60.0, -6.5, energyf, rotation=(0, 0, -35), pivot=(-14.0, 58.0, -7.0))
    ball(m, ar, (-6.0, 22.0, -11.0), 2.4, energyf, layers=3)                               # glowing orb
    return m
