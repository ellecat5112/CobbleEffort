"""Butterflamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the butterfly maiden in armour. A slim figure in rounded golden armour with a pointed spiral-
crested helm and green eyes, four great pale lilac butterfly wings ringed with violet eye-spots, navy joints, and
huge clawed red-and-gold striped gauntlets and greaves. 25 blocks tall.

Front is -z, y is up. 62 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid
from _digidetail import armour, cutout, local, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a slim figure in rounded golden armour with a spiral-crested helm, four pale lilac butterfly wings with "
        "violet eye-spots and huge clawed red-and-gold striped gauntlets")
BASE = {"gold": (250, 210, 40), "gold_dark": (190, 140, 10), "gold_light": (255, 246, 160), "red": (210, 50, 40),
        "red_dark": (130, 20, 16), "navy": (40, 50, 110), "lilac": (230, 226, 250), "lilac_dark": (190, 180, 230),
        "violet": (90, 70, 170), "violet_dark": (40, 26, 100), "claw": (240, 240, 246), "eye": (80, 220, 120)}
SHINY = {"gold": (240, 240, 250), "gold_dark": (170, 170, 190), "gold_light": (255, 255, 255), "violet": (230, 90, 140),
         "violet_dark": (140, 30, 80), "lilac": (250, 230, 236)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light")
NAVY = solid(P, "navy")


def striped(x, y, z, face, variant, box=None, **k):
    """Gold gauntlet plates with red tiger stripes."""
    p = P(variant)
    if (y * 0.8 + abs(x) * 0.5 + z * 0.3) % 3.0 < 1.0:
        return tone(p["red"], face), None
    return GOLD(x, y, z, face, variant, box=box, **k)


def wing_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5
    return a * a / 0.25 + b * b / 0.25 < 1.0


def wingf(x, y, z, face, variant, box=None, **k):
    """A lilac wing with a ring of violet eye-spot and a violet edge."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5
    r = math.hypot(a, b) * 2
    if r > 0.86:
        return tone(p["violet"], face), None
    d = math.hypot(a - 0.05, b + 0.05) * 2
    if 0.34 < d < 0.48 or d < 0.16:
        return tone(p["violet_dark"] if d < 0.16 else p["violet"], face), None
    return tone(p["lilac"] if r < 0.6 else p["lilac_dark"], face), None


def build():
    m = Model("butterflamon")
    mats = {"skin": NAVY, "chest": GOLD, "abs": GOLD, "pelvis": GOLD, "deltoid": GOLD, "upper_arm": NAVY,
            "forearm": striped, "hand": striped, "finger": GOLD, "claw": solid(P, "claw"), "thigh": NAVY,
            "knee": GOLD, "shin": striped, "calf": striped, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=1.0, leg_bulk=1.0, claws=True, name="butterflamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.4, 60.8, GOLD, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.3 - 0.6, 57.4, -3.5, sx * 1.3 + 0.6, 58.2, -3.3, solid(P, "eye", glow=True))
    spike(m, hd, (0, 60.6, -0.6), (0, 1, 0.1), 3.4, 6.0, GOLD, tip=1.0)                  # pointed spiral crest
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.8, 58.0, 0), (sx, 0.4, 0.2), 1.4, 2.4, GOLD)
    for nm in ("arm_left", "arm_right"):                                               # huge clawed gauntlets
        ab = a[nm]
        el, h = ab["elbow"], ab["hand"]
        sx = 1 if nm == "arm_left" else -1
        m.round_box(ab["bone"], h[0] + sx * 0.6, h[2], 3.6, 3.6, h[1] - 3.0, el[1] - 2.0, striped, cut=1)
        for j in range(3):
            spike(m, ab["bone"], (h[0] + sx * 0.6 + (j - 1) * 2.0, h[1] - 3.0, h[2] - 2.0), (0, -0.6, -1), 1.4,
                  4.0, solid(P, "claw"), tip=0.4)
    for sx in (-1, 1):
        dome(m, bd, (sx * 7.4, 47.0, 0.3), 3.4, 3.0, GOLD, layers=3)
    wb = m.bone("wings", bd, (0, 47, 3))                                               # four butterfly wings
    WING = cutout(wing_in, wingf)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 1.0, sx * 17.0))
        m.box(wb, x0, 46.0, 4.0, x1, 70.0, 4.0, WING, rotation=(0, sx * 20, -sx * 18), pivot=(sx * 1.0, 47.0, 4.0))
        x0, x1 = sorted((sx * 1.0, sx * 13.0))
        m.box(wb, x0, 30.0, 4.4, x1, 46.0, 4.4, WING, rotation=(0, sx * 20, sx * 20), pivot=(sx * 1.0, 46.0, 4.4))
    return m
