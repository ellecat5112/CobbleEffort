"""Lavogaritamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): an upright bird-dragon of black volcanic rock split by glowing magma, with vast spiky wings tipped with fire, flaming talons and a long spiked tail.
25 blocks. Built by _lavo.make(bird=True).

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _lavo import make

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
LOOK = "an upright bird-dragon of black volcanic rock split by glowing magma, with vast spiky wings tipped with fire, flaming talons and a long spiked tail"
build = make("lavogaritamon", bird=True)
