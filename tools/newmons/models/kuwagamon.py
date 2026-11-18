"""Kuwagamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the red stag beetle: a scarlet armoured insect with two huge serrated pincers, a fanged maw, black tiger stripes, four clawed arms, two legs and two pairs of veined wings.
15 blocks tall. Built by _kuwagamon.make(x=False).

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _kuwagamon import make

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a scarlet armoured stag beetle with two huge serrated pincers, a fanged maw, four clawed arms and veined wings"
build = make("kuwagamon", x=False)
