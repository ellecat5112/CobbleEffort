"""Herakle Kabuterimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): the great Hercules beetle: a towering olive-gold armoured insect with a great curved
horn, a second horn over its back, four clear wings, four arms with heavy clawed hands and spiked legs. 35 blocks.

Front is -z, y is up. 78 units tall (the horn); Ultimate stage. Built by _herakle.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _herakle import make

HEIGHT = 78
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a towering olive-gold armoured Hercules beetle with a great curved horn, four clear wings and four clawed arms"
build = make("heraklekabuterimon", x=False)
