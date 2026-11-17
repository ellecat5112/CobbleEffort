"""Black Guilmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Guilmon's dark twin: a charcoal-grey dinosaur with red markings, a white belly with the black
Hazard emblem, bat-wing ears, fierce yellow eyes and white claws. 1 block tall.

Front is -z, y is up. 34 units tall; Child stage. Built by _guilmon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _guilmon import make

HEIGHT = 34
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "a charcoal-grey dinosaur with red markings, a white belly with the Hazard emblem, bat-wing ears, yellow eyes"
build = make("blackguilmon", "child", black=True)
