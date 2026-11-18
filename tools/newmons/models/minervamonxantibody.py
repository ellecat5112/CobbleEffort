"""Minervamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Minervamon changed by the X-Antibody: gold-and-silver armour, a feathered crest, two great blue spiked orbs swinging on beaded chains from her shoulders and a ring of water round her sword Olympia. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built covered (a tunic over armour). Built by
_minervamon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _minervamon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Minervamon changed by the X-Antibody: gold-and-silver armour, a feathered crest, two great blue spiked orbs swinging on beaded chains from her shoulders and a ring of water round her sword Olympia"
build = make("minervamonxantibody", x=True)
