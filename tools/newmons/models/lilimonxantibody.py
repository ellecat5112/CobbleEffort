"""Lilimon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Lilimon awakened by the X-Antibody: a flower fairy in a full ruffled pink-and-yellow petal skirt with long trailing petals, long green hair, leaf wings and a yellow lily in hand.
25 blocks tall. Built by _lilimon.make(x=True), fully clothed as drawn.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _lilimon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a flower fairy in a full ruffled pink-and-yellow petal skirt with long trailing petals, long green hair, leaf wings and a yellow lily in hand"
build = make("lilimonxantibody", x=True)
