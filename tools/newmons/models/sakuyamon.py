"""Sakuyamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a warrior priestess in violet-and-gold armour with a gold fox mask, a silver mane, a golden ringed staff and four little fox spirits.
35 blocks. Built by _sakuyamon.make(look="base").

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _sakuyamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a warrior priestess in violet-and-gold armour with a gold fox mask, a silver mane, a golden ringed staff and four little fox spirits"
build = make("sakuyamon", look="base")
