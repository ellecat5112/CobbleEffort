"""Toropiamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a tropical plant beast-man: a lizard-bird head in green and gold scales with a crest of red
and yellow petals, a pink petal ruff, a brown-and-green muscled body under leaf armour, pineapple-scale gauntlets
and greaves, turquoise talons, a great split monstera leaf wing, curling feelers and a long leafy tail tipped with a
red heliconia flower. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, scales, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a tropical plant beast-man with a petal-crested lizard head, pineapple-scale gauntlets, turquoise talons, a monstera leaf wing and a flower-tipped tail"
BASE = {"green": (80, 160, 60), "green_dark": (30, 90, 30), "brown": (130, 90, 50), "brown_dark": (70, 44, 20),
        "gold": (240, 200, 60), "gold_dark": (180, 130, 20), "red": (220, 40, 40), "yellow": (250, 220, 60),
        "pink": (240, 110, 160), "teal": (60, 200, 210), "leaf": (60, 150, 60), "leaf_dark": (20, 80, 30),
        "eye": (250, 220, 50), "cream": (240, 230, 190)}
SHINY = {"green": (60, 140, 170), "green_dark": (20, 80, 110), "leaf": (60, 130, 170), "leaf_dark": (20, 70, 110)}


def P(v):
    return pal(BASE, SHINY, v)


PINE = scales(P, "gold", "gold_dark", size=1.2)
GREEN = scales(P, "green", "green_dark", size=1.0)
LEAF = skin(P, "leaf", dark="leaf_dark")


def monstera(x, y, z, face, box):
    if box is None:
        return True
    u = (x - box.lo[0]) / max(box.size[0], 1e-6)
    v = (y - box.lo[1]) / max(box.size[1], 1e-6)
    if abs(u - 0.5) > 0.5 * math.sin(v * math.pi) + 0.05:
        return False
    return (v * 7.0 + abs(u - 0.5) * 3.0) % 1.0 > 0.18 or abs(u - 0.5) < 0.12


def build():
    m = Model("toropiamon")
    mats = {"skin": skin(P, "brown", dark="brown_dark"), "chest": GREEN, "abs": skin(P, "cream", dark="brown"),
            "pelvis": LEAF, "deltoid": PINE, "upper_arm": GREEN, "forearm": PINE, "hand": GREEN, "thigh": GREEN,
            "knee": PINE, "shin": PINE, "calf": PINE, "foot": skin(P, "cream", dark="brown"), "talon": solid(P, "teal"),
            "claw": solid(P, "teal"), "neck": GREEN}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.05, digitigrade=True, claws=True, talons=True,
                 name="toropiamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.0, 4.4, 54.0, 60.0, GREEN, cut=1)
    m.round_box(hd, 0, -6.0, 2.0, 2.4, 54.6, 57.6, PINE, cut=1)                          # snout
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.4, sx * 3.1), 58.0, -4.0, max(sx * 1.4, sx * 3.1), 59.0, -3.0, solid(P, "eye", glow=True))
        pts = [(sx * 1.0, 60.0, -4.0), (sx * 2.0, 64.0, -6.0), (sx * 3.4, 65.0, -4.0)]     # curling feelers
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.3)
    for j in range(7):                                                                  # petal crest
        ang = (j - 3) * 0.35
        spike(m, hd, (math.sin(ang) * 2.0, 59.6, 1.0), (math.sin(ang) * 0.6, 0.5, 1), 2.0, 8.0 - abs(j - 3),
              solid(P, "red" if j % 2 else "yellow"), tip=0.8)
    for i in range(8):                                                                  # pink petal ruff
        ang = i * 2 * math.pi / 8
        spike(m, bd, (3.4 * math.sin(ang), 52.0, 3.0 * math.cos(ang)), (math.sin(ang), 0.4, math.cos(ang)), 2.4, 4.0,
              solid(P, "pink"), tip=0.8)
    wb = m.bone("wing_left", bd, (3.0, 48.0, 3.0))                                       # monstera leaf wing
    m.box(wb, 3.0, 36.0, 4.0, 24.0, 62.0, 4.4, cutout(monstera, LEAF), rotation=(0, -20, -30), pivot=(3.0, 48.0, 4.0))
    wr = m.bone("wing_right", bd, (-3.0, 48.0, 3.0))
    m.box(wr, -16.0, 38.0, 4.0, -3.0, 54.0, 4.4, cutout(monstera, LEAF), rotation=(0, 20, 25), pivot=(-3.0, 48.0, 4.0))
    tl = m.bone("tail", bd, (0, 30, 4))
    pts = [(0, 30.0, 4.0), (6.0, 20.0, 12.0), (14.0, 14.0, 16.0), (20.0, 20.0, 18.0), (22.0, 30.0, 18.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 2 if i < 2 else 1, GREEN, extend=0.5)
    for j in range(5):                                                                  # heliconia flower
        spike(m, tl, (22.0, 30.0 + j * 1.6, 18.0), ((-1) ** j * 1.0, 0.4, 0), 1.0, 3.0, solid(P, "red"), tip=0.8)
    return m
