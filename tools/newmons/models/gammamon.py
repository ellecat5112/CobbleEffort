"""Gammamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
fluffy little white beast of Digimon Ghost Game: three grey horns tipped red, big yellow eyes, a blue bandana, a red
band on its leg, a blue-flamed tail and violet claws. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall. Built by _gammamon.make(stage="child").
"""
from __future__ import annotations

from _digi import sized
from _gammamon import make

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a fluffy little white beast with red-tipped horns, big yellow eyes, a blue bandana and a blue-flamed tail"
build = make("gammamon", "child")
