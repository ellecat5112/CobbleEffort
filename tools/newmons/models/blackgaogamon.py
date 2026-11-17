"""Black Gaogamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Gaogamon's dark twin: a hunched charcoal wolf-beast with a great golden mane, red fighting
gloves on its forelegs, yellow eyes and a jointed steel tail ending in a pincer. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage. Built by _gaogamon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _gaogamon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a hunched charcoal wolf-beast with a great golden mane, red fighting gloves and a jointed steel pincer tail"
build = make("blackgaogamon", "adult", black=True)
