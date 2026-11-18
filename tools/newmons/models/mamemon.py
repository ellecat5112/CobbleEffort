"""Mamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the tiny powerhouse: a small round silver head with big round eyes and a cheeky grin, a red ball body and two huge red mechanical boxing fists.
25 blocks tall. Built by _mamemon.make(x=False).

Front is -z, y is up. 22 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _mamemon import make

HEIGHT = 22
SCALE, HITBOX = sized(25, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a small round silver head with big round eyes and a cheeky grin, a red ball body and two huge red mechanical boxing fists"
build = make("mamemon", x=False)
