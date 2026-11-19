"""Shademon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a living shadow of flickering black smoke torn into flame-like tongues, set with silver-ringed red spiral eyes.
15 blocks. Built by _shademon.make(nene=False).

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _shademon import make

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a living shadow of flickering black smoke torn into flame-like tongues, set with silver-ringed red spiral eyes"
build = make("shademon", nene=False)
