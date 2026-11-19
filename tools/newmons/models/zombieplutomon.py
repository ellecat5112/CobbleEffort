"""Zombie Plutomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Plutomon risen undead: its spiked armour rotted to a bruised violet-black with tarnished
green-gold trim, a single glowing green eye, a vast tattered maroon cape, a chain whip, and a long blade of sickly
green light in its claw. 35 blocks.

Front is -z, y is up. Ultimate stage. Built by _plutomon.make, recoloured.
"""
from __future__ import annotations

from _boxmodel import spike
from _digi import sized
from _digidetail import solid
from _route import pal
from _variant import clone

_Z = clone("_plutomon", "zombieplutomon",
           base={"black": (70, 50, 80), "black_dark": (26, 16, 32), "gold": (150, 150, 90), "gold_dark": (80, 80, 40),
                 "cape": (110, 30, 50), "cape_dark": (50, 10, 20), "eye": (90, 255, 120), "bone": (200, 190, 170)},
           shiny={"black": (90, 110, 90), "black_dark": (40, 50, 40), "cape": (60, 60, 80), "cape_dark": (24, 24, 34)})
HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an undead knight in rotted violet-black spiked armour with a glowing green eye, a tattered maroon cape and a green light blade"
_X = {"blade": (140, 255, 120, 200)}


def P(v):
    return pal(_X, {"blade": (255, 120, 200, 200)}, v)


_body = _Z.make("zombieplutomon", fusion=False)


def build():
    m = _body()
    arm = [b for b in m.boxes if b.bone == "arm_left"]
    lo = min(arm, key=lambda b: b.lo[1])
    h = (lo.lo[0] + lo.size[0] / 2, lo.lo[1], lo.lo[2] + lo.size[2] / 2)
    spike(m, "arm_left", h, (0.4, 1, -0.3), 1.6, 24.0, solid(P, "blade", glow=True), tip=0.8)
    return m
