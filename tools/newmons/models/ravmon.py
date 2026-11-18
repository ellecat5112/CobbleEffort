"""Ravmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
raven-man warrior in navy-and-steel armour with a red-beaked raven helm, ragged black wings and a barrel launcher.
35 blocks. Built by _ravmon.make(burst=False).

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _ravmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a raven-man warrior in navy-and-steel armour with a red-beaked raven helm, ragged black wings and a barrel launcher"
build = make("ravmon", burst=False)
