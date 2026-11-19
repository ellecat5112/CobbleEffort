"""Shakomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a pink-and-black fanged clam shell gaping open with yellow eyes peeking out and a fuzzy green blob inside.
1 block. Built by _shakomon.make(x=False).

Front is -z, y is up. 14 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _shakomon import make

HEIGHT = 14
SCALE, HITBOX = sized(1, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a pink-and-black fanged clam shell gaping open with yellow eyes peeking out and a fuzzy green blob inside"
build = make("shakomon", x=False)
