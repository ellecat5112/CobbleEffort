"""Kodokugumon Baby (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a fuzzy black spider with a shaggy orange mane round a yellow many-eyed face plate, a fanged maw, a banded abdomen and eight red-clawed legs.
Baby II stage, 0.5 blocks tall. Built by _kodoku.make(child=False).

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

from _digi import sized
from _kodoku import make

HEIGHT = 20
SCALE, HITBOX = sized(0.5, HEIGHT, 2.4)
KIND = "quadruped"
K = 4
LOOK = "a fuzzy black spider with a shaggy orange mane round a yellow many-eyed face plate, a fanged maw, a banded abdomen and eight red-clawed legs"
build = make("kodokugumonbaby", child=False)
