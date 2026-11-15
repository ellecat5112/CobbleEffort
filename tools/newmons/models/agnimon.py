"""Agnimon (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a warrior
of flame in red armour over black, a golden mane streaming back from its helmet, gold trim, and flames flickering at
its wrists and ankles. 15 blocks tall.

Front is -z, y is up. 42 units tall; Adult (Hybrid) stage.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _digi import sized
from _digiwar import make_palette, warrior

HEIGHT = 42
SCALE, HITBOX = sized(15, HEIGHT, 1.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 16}
LOOK = "a warrior of flame in red armour over black, a golden mane streaming back, gold trim and flames at its wrists and ankles"

BASE = {"suit": (40, 36, 40), "armour": (214, 50, 30), "armour_dark": (150, 30, 20), "skin": (250, 210, 180),
        "boot": (214, 50, 30), "eye": (90, 200, 250), "mane": (250, 210, 60), "mane_dark": (220, 160, 30),
        "gold": (240, 196, 60), "flame": (255, 140, 30), "flame2": (255, 220, 80)}
SHINY = {"armour": (40, 90, 200), "armour_dark": (24, 54, 140), "boot": (40, 90, 200), "mane": (230, 230, 240),
         "mane_dark": (180, 184, 196), "flame": (60, 160, 255), "flame2": (160, 220, 255)}
P = make_palette(BASE, SHINY)


def build():
    m, b, solid = warrior("agnimon", P, {"suit": "suit", "armour": "armour", "armour_dark": "armour_dark",
                                         "skin": "skin", "boot": "boot"}, bulk=1.05)
    hd = b["head"]
    for i, (dx, dy) in enumerate(((0, 0), (-1.4, -0.8), (1.4, -0.8), (-0.8, 0.9), (0.8, 0.9), (0, -1.8))):
        rod(m, hd, (dx, 36.5 + dy, 1.5), (dx * 2.2, 33.0 + dy * 2, 9.0 + abs(dx)), 1.6,
            solid("mane" if i % 2 == 0 else "mane_dark"), extend=0.3)
    spike(m, hd, (0, 37.6, -1.6), (0, 1, 0.3), 1.4, 2.6, solid("gold"), tip=0.3)
    m.box(b["body"], -1.4, 28.0, -2.8, 1.4, 31.0, -2.5, solid("gold"))                 # chest emblem
    for nm, sx, y in (("arm_left", 1, 20.0), ("arm_right", -1, 20.0)):
        for d in ((0, 1, -0.3), (sx * 0.6, 1, 0.3)):
            spike(m, b[nm], (sx * 5.6, y + 1.0, -0.6), d, 1.4, 3.4, solid("flame", glow=True), tip=0.3)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        spike(m, b[nm], (sx * 2.1, 2.4, 0.4), (sx * 0.5, 1, 0.6), 1.4, 3.2, solid("flame2", glow=True), tip=0.3)
    return m
