"""Muso Knightmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the warrior knight of two cannons: a broad knight in black armour trimmed with gold, a gold-crested
black helm with a V crown, green gems in its shoulder guards, a tattered black cape spreading like wings, a huge grey
cannon mounted on each arm with a red-lit barrel, black spikes jutting from its plates and gold legs. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, gem, local, metal, noise2, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a broad black-and-gold armoured knight with a V-crowned helm, a tattered black cape and a huge grey cannon on each arm"
BASE = {"black": (40, 40, 48), "black_dark": (12, 12, 16), "black_light": (110, 110, 130), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "gold_light": (255, 240, 170), "grey": (160, 164, 176), "grey_dark": (70, 74, 86),
        "green": (60, 220, 140), "green_light": (200, 255, 220), "red": (230, 40, 50), "eye": (250, 220, 60)}
SHINY = {"black": (230, 230, 240), "black_dark": (150, 150, 166), "black_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.3)
GOLD = armour(P, "gold", "gold_dark", light="gold_light")
GUN = metal(P, "grey", dark="grey_dark")


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.18 * abs(math.sin(u * 0.7)) + 0.08 * noise2(u, 0.0, 3)


def build():
    m = Model("musoknightmon")
    mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": GOLD, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": GOLD, "knee": GOLD, "shin": GOLD, "calf": GOLD,
            "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.3, leg_bulk=1.15, name="musoknightmon")
    bd = a["body"]
    cape(m, bd, 53.0, 22.0, 46.0, cutout(tatter, fabric(P, "black", "black_dark")), z=4.4, flare=1.2, panels=10, sweep=(0.0, 4.0))
    for sx in (-1, 1):                                                               # shoulder guards + gems
        m.round_box(bd, sx * 9.0, 0, 4.0, 4.4, 46.0, 54.0, GOLD, cut=2)
        m.round_box(bd, sx * 9.0, -4.6, 1.2, 0.4, 49.0, 51.4, gem(P, "green", "green_light"), cut=0)
        for j in range(3):
            spike(m, bd, (sx * 10.0, 50.0 - j * 6.0, 2.0), (sx, 0.3, 0.5), 1.2, 6.0, solid(P, "black"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -0.6, 2.8, 3.2, 54.0, 61.0, ARM, cut=1)
    m.round_box(hd, 0, -3.8, 2.0, 0.3, 56.6, 57.8, solid(P, "eye", glow=True), cut=0)
    for sx in (-1, 1):                                                               # V crown
        rod(m, hd, (0, 60.6, -2.6), (sx * 5.0, 67.0, -2.0), 1, metal(P, "gold", dark="gold_dark"), extend=0.2, t2=2)
    spike(m, hd, (0, 61.0, -2.4), (0, 1, 0), 1.4, 4.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for nm in ("arm_left", "arm_right"):                                              # huge arm cannons
        w = a[nm]["wrist"]
        sx = 1 if w[0] > 0 else -1
        m.round_box(a[nm]["bone"], w[0] + sx * 1.0, w[2] - 4.0, 5.0, 8.0, w[1] - 4.0, w[1] + 4.6, GUN, cut=2)
        m.round_box(a[nm]["bone"], w[0] + sx * 1.0, w[2] - 12.4, 3.0, 0.6, w[1] - 2.4, w[1] + 3.0, solid(P, "black_dark"), cut=0)
        m.round_box(a[nm]["bone"], w[0] + sx * 1.0, w[2] - 12.6, 1.4, 0.3, w[1] - 0.6, w[1] + 1.2, solid(P, "red", glow=True), cut=0)
    return m
