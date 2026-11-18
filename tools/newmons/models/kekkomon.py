"""Kekkomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby II round green spiky slime with a crescent-moon mark, a tall pink-tipped spike, spiky frills and a red tuft.
Baby II stage, 0.5 blocks tall. Built by _kekomon.make(crest=True).

Front is -z, y is up. 14 units tall.
"""
from __future__ import annotations

from _digi import sized
from _kekomon import make

HEIGHT = 14
SCALE, HITBOX = sized(0.5, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a Baby II round green spiky slime with a crescent-moon mark, a tall pink-tipped spike, spiky frills and a red tuft"
build = make("kekkomon", crest=True)
