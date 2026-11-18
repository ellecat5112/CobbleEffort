"""Kekomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby I round green spiky slime with a yellow belly lip, big round eyes, a happy open mouth and a tall pink-tipped spike.
Baby I stage, 0.35 blocks tall. Built by _kekomon.make(crest=False).

Front is -z, y is up. 14 units tall.
"""
from __future__ import annotations

from _digi import sized
from _kekomon import make

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a Baby I round green spiky slime with a yellow belly lip, big round eyes, a happy open mouth and a tall pink-tipped spike"
build = make("kekomon", crest=False)
