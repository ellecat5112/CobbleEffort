"""Siesamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a white-and-gold shisa guardian with a spiral golden mane, a single horn, cloud-swirl fur and a huge curling golden tail.
15 blocks. Built by _siesamon.make(x=False).

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _siesamon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a white-and-gold shisa guardian with a spiral golden mane, a single horn, cloud-swirl fur and a huge curling golden tail"
build = make("siesamon", x=False)
