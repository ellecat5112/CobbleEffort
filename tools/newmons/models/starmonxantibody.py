"""Starmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a pale-lilac layered star with red-and-blue star-spangled gloves and boots and a long yellow ribbon scarf.
15 blocks. Built by _starmon.make(x=True).

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _starmon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a pale-lilac layered star with red-and-blue star-spangled gloves and boots and a long yellow ribbon scarf"
build = make("starmonxantibody", x=True)
