"""Achillesmon (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a lean
warrior in black with golden armour on its chest, arms and shins, a tall white-and-purple plumed helmet, a long golden
spear, and round golden shields at its heels from which cyan wings of light flare out. 35 blocks tall.

Front is -z, y is up. 46 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _digi import sized
from _digiwar import make_palette, warrior

HEIGHT = 46
SCALE, HITBOX = sized(35, HEIGHT, 1.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 16}
LOOK = ("a lean warrior in black with golden armour, a tall white-and-purple plumed helmet, a long golden spear and "
        "round golden heel-shields flaring cyan wings of light")

BASE = {"suit": (40, 40, 48), "armour": (240, 196, 40), "armour_dark": (176, 130, 20), "skin": (40, 40, 48),
        "boot": (240, 196, 40), "eye": (255, 80, 80), "plume": (150, 70, 200), "plume_light": (240, 240, 250),
        "wing": (90, 230, 240, 150), "spear": (230, 190, 60), "tip": (240, 240, 250)}
SHINY = {"armour": (210, 214, 226), "armour_dark": (150, 156, 170), "boot": (210, 214, 226), "plume": (220, 60, 60),
         "wing": (255, 160, 70, 150), "spear": (210, 214, 226)}
P = make_palette(BASE, SHINY)


def plumef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
    return (p["plume_light"] if int(t * 6) % 2 else p["plume"]), None


def wingf(x, y, z, face, variant, **k):
    """A heel wing of cyan light (a cut-out plane in the yz plane), feathered at its tips."""
    p = P(variant)
    u, v = z - 1.0, y                                          # back and up from the heel
    if not (0 < u < 9 and abs(v - 1.5 - u * 0.55) < 2.6 - u * 0.2) or (u > 5 and (u + v) % 2 < 0.6):
        return (0, 0, 0, 0), None
    return p["wing"], None


def build():
    m, b, solid = warrior("achillesmon", P, {"suit": "suit", "armour": "armour", "armour_dark": "armour_dark",
                                             "skin": "skin", "boot": "boot"}, bulk=0.95)
    hd = b["head"]
    for i in range(5):                                         # the tall plume
        rod(m, hd, (0, 37.0 + i * 0.4, 1.0 + i * 0.6), (0, 41.0 + i * 1.0, 3.0 + i * 1.6), 1.4 - i * 0.15, plumef,
            extend=0.2, t2=0.6)
    sp = m.bone("spear", b["arm_left"], (5.2, 19.0, -0.6))
    rod(m, sp, (2.0, 6.0, 4.0), (8.0, 42.0, -8.0), 0.9, solid("spear"), extend=0.0)
    spike(m, sp, (8.0, 42.0, -8.0), (0.16, 0.95, -0.3), 1.6, 4.0, solid("tip"), tip=0.3)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = b[nm]
        m.box(lg, sx * 2.0 - 1.6, 0.5, 1.4, sx * 2.0 + 1.6, 3.7, 2.0, solid("armour"))        # round heel shields
        m.box(lg, sx * 3.0, 0.0, 1.0, sx * 3.0, 9.0, 11.0, wingf, rotation=(0, sx * 20, 0), pivot=(sx * 3.0, 0, 1.0))
    return m
