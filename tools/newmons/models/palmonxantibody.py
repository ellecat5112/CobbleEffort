"""Palmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Palmon changed by the X-Antibody: a rainbow flower of blue, yellow and pink petals, a blue leaf cape and a seed pendant. 1 block tall.

Front is -z, y is up. 24 units tall; Child stage. Built by _palmon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _palmon import make

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "Palmon changed by the X-Antibody: a rainbow flower of blue, yellow and pink petals, a blue leaf cape and a seed pendant"
build = make("palmonxantibody", x=True)
