"""Gankoomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): Gankoomon awakened by the X-Antibody: the warrior bare-chested as officially drawn,
spiky red-and-gold hair, a white-and-grey hakama with silver greaves and red-clawed boots, a red cross relic at his
hip, wrapped in golden flame. 35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage. Built by _gankoomon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _gankoomon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a warrior with spiky red-and-gold hair, a white hakama and silver greaves, wrapped in golden flame"
build = make("gankoomonxantibody", x=True)
