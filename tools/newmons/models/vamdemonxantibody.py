"""Vamdemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Vamdemon changed by the X-Antibody: a black suit with a crimson waistcoat, a ragged red-lined cape
tipped with pink crystal claws, a purple fur collar, blond hair and a chain across its chest. 25 blocks.

Front is -z, y is up. Perfect stage. Built by _vamdemon.make.
"""
from __future__ import annotations

from _digi import sized
from _vamdemon import make

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a vampire lord in a black suit with a ragged red-lined cape tipped with pink crystal claws and blond hair"
build = make("vamdemonxantibody", True)
