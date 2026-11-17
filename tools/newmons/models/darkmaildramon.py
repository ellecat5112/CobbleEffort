"""Dark Maildramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the armoured dragon of darkness. A sitting dragon cased in glossy black plate with gold rims, a
long arched neck ending in a knight's helm with a tall spike and a tuft of blonde hair, round armoured shoulders and
haunches, a red gem on its chest, gold-clawed feet, a segmented tail and two ragged dark-red wings. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome
from _digibeast import bat_wing
from _digidetail import armour, cutout, gem, local, metal, noise2, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a sitting dragon in glossy black plate with gold rims, a long neck ending in a spiked knight's helm, a red "
        "chest gem, gold-clawed feet and ragged dark-red wings")
BASE = {"black": (44, 44, 52), "black_dark": (14, 14, 18), "black_light": (130, 132, 150), "gold": (220, 170, 80),
        "gold_dark": (150, 100, 30), "red": (210, 30, 30), "red_light": (255, 150, 140), "wing": (110, 24, 24),
        "wing_dark": (60, 8, 8), "hair": (240, 220, 120), "hair_dark": (190, 160, 60), "steel": (200, 200, 210),
        "steel_dark": (100, 100, 110)}
SHINY = {"black": (230, 230, 236), "black_dark": (150, 150, 160), "black_light": (255, 255, 255),
         "wing": (40, 60, 140), "wing_dark": (14, 24, 70)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.35)
GOLD = metal(P, "gold", dark="gold_dark")


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["wing_dark"] if noise2(u * 0.5, v * 0.5, 2) > 0.6 else p["wing"], face), None


def ragged(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.12 * (1 + math.sin(u * 2.1)) + 0.1 * noise2(u * 0.9, 0, 5)


def build():
    m = Model("darkmaildramon")
    top = m.bone("darkmaildramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 2.0, 7.0, 8.0, 10.0, 22.0, PLATE, cut=2)                          # haunch-heavy body
    m.round_box(bd, 0, -1.0, 6.0, 6.4, 20.0, 30.0, PLATE, cut=2)                          # chest
    m.round_box(bd, 0, -7.2, 1.8, 0.8, 24.0, 27.6, gem(P, "red", "red_light"), cut=1)
    nk = m.bone("neck", bd, (0, 30, -1))
    pts = [(0, 29.0, -1.0), (0, 34.0, -2.0), (0, 38.0, -1.0), (0, 41.0, 1.0), (0, 43.0, -1.0)]
    for p0, p1 in zip(pts, pts[1:]):                                                     # arched neck
        rod(m, nk, p0, p1, 4, PLATE, extend=0.6)
    hd = m.bone("head", nk, (0, 43, -1))
    m.round_box(hd, 0, -3.0, 2.8, 4.6, 41.0, 46.0, PLATE, cut=1)                         # knight's helm
    m.box(hd, -2.4, 42.6, -7.8, 2.4, 43.4, -7.4, solid(P, "black_dark"))                 # visor slit
    spike(m, hd, (0, 46.0, -3.0), (0, 1, 0.1), 1.6, 6.0, GOLD, tip=0.2)                  # tall spike
    for i in range(6):                                                                   # blonde tuft
        rod(m, hd, ((i - 2.5) * 0.6, 45.6, 0.6), ((i - 2.5) * 1.2, 44.0, 5.0), 1, strands(P, "hair", "hair_dark"),
            extend=0.2)
    for sx in (-1, 1):
        dome(m, bd, (sx * 6.4, 26.0, -1.0), 3.0, 3.0, PLATE)                             # round shoulders
        dome(m, bd, (sx * 6.6, 16.0, 3.0), 4.0, 4.0, PLATE)                              # round haunches
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        lg = m.bone(nm, bd, (sx * 5.0, 24.0, -3.0))
        rod(m, lg, (sx * 5.0, 24.0, -3.0), (sx * 5.0, 3.0, -5.0), 3, PLATE, extend=0.4)
        m.box(lg, sx * 5.0 - 2.0, 0.0, -8.0, sx * 5.0 + 2.0, 3.0, -3.0, PLATE)
        for j in range(3):
            spike(m, lg, (sx * 5.0 + (j - 1) * 1.3, 1.0, -8.0), (0, -0.1, -1), 1.2, 3.0, GOLD, tip=0.25)
    for sx, nm in ((1, "leg_back_left"), (-1, "leg_back_right")):
        lg = m.bone(nm, bd, (sx * 7.0, 12.0, 4.0))
        m.round_box(lg, sx * 8.0, -2.0, 2.6, 4.6, 0.0, 4.0, PLATE, cut=1)
        for j in range(4):
            spike(m, lg, (sx * 8.0 + (j - 1.5) * 1.3, 1.0, -6.4), (sx * 0.2 * (j - 1.5), -0.1, -1), 1.2, 3.6, GOLD,
                  tip=0.25)
    tl = m.bone("tail", bd, (0, 12, 8))
    for j in range(6):                                                                   # segmented tail
        ang = j * 0.5
        p0 = (-j * 2.4, 6.0 - j * 0.6, 8.0 + 3.0 * math.cos(ang))
        m.round_box(tl, p0[0], p0[2], 2.4 - j * 0.25, 2.4 - j * 0.25, max(0.2, p0[1] - 2.0), p0[1] + 2.0, PLATE, cut=1)
    spike(m, tl, (-13.0, 3.0, 5.6), (-1, 0, -0.4), 1.2, 4.0, GOLD)
    for side in (1, -1):                                                                 # ragged wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 28.0, 4.0))
        bat_wing(m, wb, (side * 4.0, 28.0, 4.0), 16.0, 20.0, 3, PLATE, cutout(ragged, wingf), side=side, sweep=20)
    return m
