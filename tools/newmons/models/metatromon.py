"""Metatromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an angelic machine of gold and silver: a tall armoured mechanical body of silver plates trimmed
gold with round lenses at its joints and chest, a gold-crested head under a halo of light, long armoured legs ending in
pointed gold-trimmed feet, and two vast fanned wings made of steel key-blades, each with a lens at its hilt. 35 blocks
tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("an angelic machine of silver plates trimmed gold with lenses at its joints, a gold-crested head under a halo "
        "and two vast fanned wings of steel key-blades")
BASE = {"silver": (210, 214, 226), "silver_dark": (110, 116, 136), "gold": (230, 180, 60), "gold_dark": (150, 110, 20),
        "black": (30, 30, 36), "lens": (110, 150, 220), "lens_light": (220, 236, 255), "halo": (200, 230, 255, 170)}
SHINY = {"silver": (60, 60, 72), "silver_dark": (24, 24, 30), "gold": (200, 210, 230), "gold_dark": (120, 130, 150)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")
LENS = gem(P, "lens", "lens_light")


def build():
    m = Model("metatromon")
    mats = {"skin": ARM, "neck": solid(P, "black"), "upper_arm": metal(P, "silver"), "thigh": metal(P, "silver"),
            "knee": GOLD, "hand": GOLD, "finger": GOLD, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=0.9, leg_bulk=1.0, name="metatromon")
    bd = a["body"]
    ball(m, bd, (0, 46.0, -4.2), 1.8, LENS, layers=2)
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):
        anc = a[nm]
        j = anc.get("elbow") or anc.get("knee")
        ball(m, anc["bone"], (j[0], j[1], j[2] - 1.2), 1.4, LENS, layers=2)
    for nm in ("leg_left", "leg_right"):                                                  # pointed feet
        ank = a[nm]["ankle"]
        spike(m, a[nm]["bone"], (ank[0], 1.0, ank[2] - 2.0), (0, -0.3, -1), 2.4, 5.0, GOLD, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 59.6, ARM, cut=1)
    m.box(hd, -1.6, 57.0, -3.1, 1.6, 57.6, -2.9, solid(P, "lens", glow=True))
    spike(m, hd, (0, 59.4, -1.0), (0, 1, 0.2), 1.6, 5.0, GOLD, tip=0.8)                      # gold crest
    for i in range(14):                                                                   # halo of light
        ang = 2 * math.pi * i / 14
        m.box(hd, 4.0 * math.cos(ang) - 0.7, 66.0, 4.0 * math.sin(ang) - 0.7, 4.0 * math.cos(ang) + 0.7, 66.6,
              4.0 * math.sin(ang) + 0.7, solid(P, "halo", glow=True))
    for side in (1, -1):                                                                  # fanned key-blade wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 48.0, 4.0))
        for j in range(7):
            ang = math.radians(-40 + j * 20)
            root = (side * 4.0, 48.0, 4.0 + j * 0.3)
            hilt = (side * (4.0 + 12.0 * math.cos(ang)), 48.0 + 12.0 * math.sin(ang), 5.0 + j * 0.3)
            tip = (side * (4.0 + 28.0 * math.cos(ang)), 48.0 + 28.0 * math.sin(ang), 6.0 + j * 0.3)
            rod(m, wb, root, hilt, 1, metal(P, "silver_dark"), extend=0.2)
            ball(m, wb, hilt, 1.4, LENS, layers=2)
            rod(m, wb, hilt, tip, 1, ARM, extend=0.2, t2=3)
    return m
