"""Gesomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
white squid-beast with a pointed mantle painted with grey tribal marks, a wide fanged maw, two long arms with black
hooked claws and a mass of white tentacles beneath. Adult stage, 15 blocks tall.

Front is -z, y is up. 36 units tall. Built by _gesomon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _gesomon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = "a white squid-beast with a tribal-marked pointed mantle, a fanged maw and long clawed arms"
build = make("gesomon", x=False)
