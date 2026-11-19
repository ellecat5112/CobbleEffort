"""Sakuyamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a radiant priestess in white-and-gold armour with a gold fox mask, a great halo-ringed staff and a swirl of blue fox-fire.
35 blocks. Built by _sakuyamon.make(look="x").

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
LOOK = "a radiant priestess in white-and-gold armour with a gold fox mask, a great halo-ringed staff and a swirl of blue fox-fire"
build = make("sakuyamonxantibody", look="x")
