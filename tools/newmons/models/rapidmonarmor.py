"""Rapidmon Armor (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the Armor Digimon of miracles: a round golden robot rabbit with long red-tipped rocket ears and red ball cannons.
15 blocks. Built by _rapidarmor.make(x=False).

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _rapidarmor import make

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a round golden robot rabbit with long red-tipped rocket ears, a red visor and red-spiked ball cannons for hands"
build = make("rapidmonarmor", x=False)
