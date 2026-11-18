"""Lavorvomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a low four-legged dragon of black volcanic rock split by glowing magma cracks, with yellow horns and claws, a spiny back and a hooked yellow tail tip.
15 blocks. Built by _lavo.make(bird=False).

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _lavo import make

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
LOOK = "a low four-legged dragon of black volcanic rock split by glowing magma cracks, with yellow horns and claws, a spiny back and a hooked yellow tail tip"
build = make("lavorvomon", bird=False)
