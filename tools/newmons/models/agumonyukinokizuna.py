"""Agumon -Yuki no Kizuna- (a Digimon of the CobbleEffort: Digital crossover, built after the official art on
wikimon.net): Agumon's courage given a warrior's form: orange armour striped blue, a dark horned helmet, long red-hot
gauntlet claws, and two great wings of fire crossing in an X behind it. 35 blocks tall.

Front is -z, y is up. 50 units tall (the fire wings); Ultimate stage.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _digi import claw_fan, sized
from _digiwar import make_palette, warrior
from _route import tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 1.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "Agumon as a warrior: orange armour striped blue, a dark horned helmet, long red-hot claws and two wings of fire crossed in an X behind it"

BASE = {"suit": (60, 50, 50), "armour": (246, 160, 40), "armour_dark": (40, 100, 200), "skin": (246, 160, 40),
        "boot": (246, 160, 40), "eye": (110, 220, 190), "helm": (70, 60, 60), "claw": (230, 60, 40),
        "fire": (255, 140, 40, 170), "fire2": (255, 200, 80, 170)}
SHINY = {"armour": (70, 70, 80), "skin": (70, 70, 80), "boot": (70, 70, 80), "armour_dark": (200, 40, 50),
         "fire": (80, 160, 255, 170), "fire2": (160, 220, 255, 170)}
P = make_palette(BASE, SHINY)


def firef(x, y, z, face, variant, box=None, **k):
    """A wing of fire (a cut-out plane): a long flame tapering to a ragged tip."""
    p = P(variant)
    lx = x - (box.lo[0] + box.size[0] / 2)
    t = (y - box.lo[1]) / max(box.size[1], 1e-6)
    if abs(lx) > (box.size[0] / 2) * (1 - t * 0.7) or (t > 0.6 and (y * 1.3 + abs(lx)) % 2.2 < 0.6):
        return (0, 0, 0, 0), None
    return (p["fire2"] if abs(lx) < box.size[0] * 0.15 else p["fire"]), None


def build():
    m, b, solid = warrior("agumonyukinokizuna", P, {"suit": "suit", "armour": "armour", "armour_dark": "armour_dark",
                                                    "skin": "skin", "boot": "boot"}, bulk=1.15)
    hd = b["head"]
    m.box(hd, -2.4, 36.0, -2.6, 2.4, 38.6, 2.4, solid("helm"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.8, 38.0, 0.0), (sx * 0.6, 1, 0.4), 1.2, 3.0, solid("helm"), tip=0.3)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):
        claw_fan(m, b[nm], (sx * 6.3, 19.0, -1.2), (0, -0.5, -1), 3, 0.9, 4.0, 0.9, key="red")
    fw = m.bone("wings", b["body"], (0, 30, 3))
    for ang in (35, -35):                                      # the X of fire
        m.box(fw, -5.0, 22.0, 3.6, 5.0, 50.0, 3.6, firef, rotation=(0, 0, ang), pivot=(0, 30, 3.6))
    return m
