"""Mephismon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a fallen angel with a goat-skull head and curled ram horns, black bat wings, a dark muscular torso, red-banded arms with huge white gloves, enormous puffy violet fur trousers and grey hooves. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built by _mephismon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _mephismon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a fallen angel with a goat-skull head and curled ram horns, black bat wings, a dark muscular torso, red-banded arms with huge white gloves, enormous puffy violet fur trousers and grey hooves"
build = make("mephismon", x=False)
