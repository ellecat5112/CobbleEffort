"""Plutomon (Fusion) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Plutomon fused with a great beast: the knight rides atop a mound of blue scales whose front is a silver
orb of a face with four black eyes. 35 blocks. Built by _plutomon.make(fusion=True).

Front is -z, y is up. 112 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _plutomon import make

HEIGHT = 112
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "Plutomon riding atop a great mound of blue scales whose front is a silver orb face with four black eyes"
build = make("plutomonfusion", fusion=True)
