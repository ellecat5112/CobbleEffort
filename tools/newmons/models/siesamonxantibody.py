"""Siesamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a gleaming golden armoured shisa with spiked silver horns, a red tasselled collar, cyan cloud swirls and a flaming tail.
15 blocks. Built by _siesamon.make(x=True).

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
LOOK = "a gleaming golden armoured shisa with spiked silver horns, a red tasselled collar, cyan cloud swirls and a flaming tail"
build = make("siesamonxantibody", x=True)
