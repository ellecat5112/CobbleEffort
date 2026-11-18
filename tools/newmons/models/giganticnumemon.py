"""Gigantic Numemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): an enormous lime-green Numemon with blue patches, bloodshot eyes on stalks, a huge mouth of big square
teeth and a long lolling pink tongue. Adult stage, 15 blocks tall.

Front is -z, y is up. 36 units tall. Built by _numemon.make("gigantic").
"""
from __future__ import annotations

from _digi import sized
from _numemon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = "an enormous lime-green slime with blue patches, eyes on stalks, a huge mouth of square teeth and a long tongue"
build = make("giganticnumemon", "gigantic")
