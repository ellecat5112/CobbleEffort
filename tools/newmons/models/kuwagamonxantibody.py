"""Kuwagamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Kuwagamon awakened by the X-Antibody: a slimmer upright red insect with long straight pincers, a wide purple maw, four clawed arms and veined wings.
15 blocks tall. Built by _kuwagamon.make(x=True).

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
build = make("kuwagamonxantibody", x=True)
