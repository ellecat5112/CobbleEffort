"""Chaos Grimmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the corrupted reaper. A lean armoured dragon-man in dark blue and crimson plate with silver
bladed edges, a horned helm crowned in pink-red crystal spikes, a long curving scythe-blade arm, red cannon gauntlet,
taloned feet and great glowing amber energy wings fanning behind it. 25 blocks tall.

Front is -z, y is up. 62 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid
from _digidetail import armour, cutout, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean dragon-man in dark blue and crimson plate with silver blade edges, a crystal-spiked helm, a long "
        "scythe-blade arm and glowing amber energy wings")
BASE = {"navy": (40, 50, 130), "navy_dark": (14, 18, 60), "navy_light": (100, 120, 210), "red": (200, 40, 50),
        "red_dark": (110, 14, 20), "silver": (210, 214, 226), "silver_dark": (110, 114, 128), "crystal": (240, 110, 140),
        "crystal_light": (255, 210, 220), "wing": (255, 200, 80, 190), "wing_core": (255, 245, 200, 220),
        "eye": (250, 230, 80), "under": (30, 30, 40)}
SHINY = {"navy": (50, 50, 56), "navy_dark": (16, 16, 20), "red": (80, 200, 230), "red_dark": (30, 120, 160),
         "wing": (140, 230, 255, 190)}


def P(v):
    return pal(BASE, SHINY, v)


NAVY = armour(P, "navy", "navy_dark", light="navy_light", trim="silver", trim_w=0.3)
RED = armour(P, "red", "red_dark", trim="silver", trim_w=0.25)
SILVER = metal(P, "silver", dark="silver_dark")


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["wing_core"] if u / max(W, 1e-6) < 0.3 else p["wing"]
    return c, c[:3]


def wing_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6)
    return b < 1.0 - a * 0.7 and b > 0.15 * a and (b * 6 + a * 2) % 1.0 > 0.15


def build():
    m = Model("chaosgrimmon")
    mats = {"skin": solid(P, "under"), "chest": NAVY, "abs": RED, "pelvis": NAVY, "deltoid": RED, "upper_arm": NAVY,
            "forearm": RED, "hand": NAVY, "finger": SILVER, "claw": SILVER, "thigh": NAVY, "knee": RED, "shin": NAVY,
            "calf": RED, "foot": NAVY, "talon": SILVER}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=1.0, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="chaosgrimmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 3.0, 54.4, 61.0, NAVY, cut=1)
    m.box(hd, -1.8, 54.6, -6.4, 1.8, 57.4, -3.0, NAVY)                                 # dragon snout
    m.box(hd, -2.0, 58.0, -3.9, 2.0, 58.6, -3.5, solid(P, "eye", glow=True))
    for j, (dx, d) in enumerate(((0, (0, 1, 0.3)), (-1.6, (-0.4, 1, 0.4)), (1.6, (0.4, 1, 0.4)),
                                  (-2.6, (-0.8, 0.8, 0.6)), (2.6, (0.8, 0.8, 0.6)))):
        spike(m, hd, (dx, 60.6, 0.0), d, 1.4, 5.0 - abs(dx) * 0.6, gem(P, "crystal", "crystal_light"), tip=0.3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = a[nm]["shoulder"]
        dome(m, a[nm]["bone"], (sh[0] + sx * 1.6, 49.4, 0.3), 3.6, 3.4, RED, layers=3)
        spike(m, a[nm]["bone"], (sh[0] + sx * 2.6, 51.4, 0.3), (sx, 0.6, 0.4), 1.6, 5.0, SILVER, tip=0.4)
    ar = a["arm_right"]                                                                # the scythe-blade arm
    h = ar["hand"]
    pts = [h, (h[0] - 4.0, h[1] + 8.0, h[2] - 6.0), (h[0] - 6.0, h[1] + 18.0, h[2] - 4.0),
           (h[0] - 4.0, h[1] + 26.0, h[2] + 2.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, ar["bone"], p0, p1, 1, SILVER, extend=0.4, t2=3)
    al = a["arm_left"]                                                                 # red cannon gauntlet
    h = al["hand"]
    rod(m, al["bone"], (h[0], h[1] + 4.0, h[2]), (h[0], h[1] - 6.0, h[2] - 4.0), 4, RED, extend=0.4)
    for sx in (-1, 1):                                                                 # amber energy wings
        x0, x1 = sorted((sx * 3.0, sx * 26.0))
        for j, ang in enumerate((25, 0, -25)):
            m.box(bd, x0, 40.0, 5.0 + j, x1, 58.0, 5.0 + j, cutout(wing_in, wingf),
                  rotation=(0, sx * 20, sx * ang), pivot=(sx * 3.0, 50.0, 5.0 + j))
    return m
