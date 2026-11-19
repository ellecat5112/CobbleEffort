"""Tyranomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Tyranomon changed by the X-Antibody: a crouching muscular red tyrannosaur with black
stripes, a row of green crystal spines down its back and tail, a white throat and steel claws. 15 blocks.

Front is -z, y is up. Adult stage. Built by _darktyranomon.make(x=True), recoloured.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_T = clone("_darktyranomon", "tyranomonxantibody",
           base={"black": (210, 40, 40), "black_dark": (120, 14, 14), "black_light": (250, 110, 100),
                 "red": (40, 30, 34)},
           shiny={"black": (60, 130, 200), "black_dark": (20, 70, 130), "black_light": (140, 200, 250)})
HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a crouching muscular red tyrannosaur with black stripes, green crystal spines and steel claws"
build = _T.make("tyranomonxantibody", x=True)
