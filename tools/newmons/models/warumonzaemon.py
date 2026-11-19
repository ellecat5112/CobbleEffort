"""Waru Monzaemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Monzaemon gone bad: a hulking charcoal-grey teddy bear with a cream belly stitched over
a glowing green heart-wound, sullen red-rimmed eyes, a red neckerchief and a ragged red cape, a riveted steel band on
one arm and long steel claws bursting from its right paw. 25 blocks.

Front is -z, y is up. Perfect stage. Built on _monzaemon.make, recoloured.
"""
from __future__ import annotations

from _boxmodel import spike
from _digi import sized
from _digibody import cape
from _digibeast import ball
from _digidetail import fabric, metal, solid
from _route import pal
from _variant import clone

_M = clone("_monzaemon", "warumonzaemon",
           base={"yellow": (80, 78, 86), "yellow_dark": (34, 32, 38), "white": (246, 236, 200), "white_dark": (200, 186, 140),
                 "cream": (230, 210, 170), "plaster": (120, 100, 70)},
           shiny={"yellow": (120, 70, 50), "yellow_dark": (60, 30, 20)})
HEIGHT = 51
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking charcoal teddy bear with a stitched glowing heart-wound, a red neckerchief and cape, and long steel claws"
_X = {"red": (200, 30, 40), "red_dark": (110, 10, 16), "steel": (210, 214, 226), "steel_dark": (110, 114, 126),
      "green": (90, 255, 120)}


def P(v):
    return pal(_X, {"red": (60, 90, 190), "red_dark": (20, 40, 110)}, v)


_body = _M.make("warumonzaemon", x=False)


def build():
    m = _body()
    ball(m, "body", (0, 24.0, -10.4), 1.2, solid(P, "green", glow=True), layers=1)          # glowing heart-wound
    m.box("body", -4.0, 33.4, -7.0, 4.0, 35.6, -6.2, solid(P, "red"))                       # neckerchief
    cape(m, "body", 35.0, 14.0, 26.0, fabric(P, "red", "red_dark"), z=8.6, flare=0.6, panels=5, seed=8)
    m.round_box("arm_left", 11.0, -1.4, 3.6, 3.6, 22.0, 25.0, metal(P, "steel", dark="steel_dark"), cut=1)
    for j in range(3):                                                                    # steel claws
        spike(m, "arm_right", (-12.4 + (j - 1) * 1.4, 18.6, -4.0), (0, -1, -0.4), 1.0, 6.0,
              metal(P, "steel", dark="steel_dark"), tip=0.8)
    return m
