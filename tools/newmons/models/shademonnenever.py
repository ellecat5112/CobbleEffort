"""Shademon (Nene Ver.) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a slender shadow figure in a long flowing black gown pooling into smoke, long silver hair in two tall bunches and a ragged black wing of eyes.
15 blocks. Built by _shademon.make(nene=True).

Front is -z, y is up. 66 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _shademon import make

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a slender shadow figure in a long flowing black gown pooling into smoke, long silver hair in two tall bunches and a ragged black wing of eyes"
build = make("shademonnenever", nene=True)
