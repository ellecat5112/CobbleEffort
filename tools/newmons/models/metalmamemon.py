"""Metal Mamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little cyborg super-soldier: a round silver ball dotted with bolt holes, big red eyes, a red mechanical claw hand and a huge arm cannon firing an orange energy ball. 25 blocks tall.

Front is -z, y is up. 20 units tall; Perfect stage. Built by _metalmamemon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _metalmamemon import make

HEIGHT = 20
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little cyborg super-soldier: a round silver ball dotted with bolt holes, big red eyes, a red mechanical claw hand and a huge arm cannon firing an orange energy ball"
build = make("metalmamemon", x=False)
