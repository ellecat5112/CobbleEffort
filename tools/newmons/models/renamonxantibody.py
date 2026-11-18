"""Renamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): an amber fox marked with crimson flames, black-violet clawed gloves and two ghostly fox spirits wreathing
it. 1 block. Built by _renamon.make(x=True).

Front is -z, y is up. 68 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _renamon import make

HEIGHT = 68
SCALE, HITBOX = sized(1, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "an amber upright fox marked with crimson flames, black-violet clawed gloves and two ghostly fox spirits wreathing it"
build = make("renamonxantibody", x=True)
