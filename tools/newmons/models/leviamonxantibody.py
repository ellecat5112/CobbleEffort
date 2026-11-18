"""Leviamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Leviamon awakened by the X-Antibody: a colossal dark violet crocodile-leviathan with huge pink blade fins, a jagged tail blade and a glowing magic circle above it. 45 blocks long (Demon Lord). Built by _leviamon.make(x=True).

Front is -z, y is up. 26 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _leviamon import make

HEIGHT = 26
SCALE, HITBOX = sized(45, HEIGHT, 10.0)
KIND = "quadruped"
K = 3
LOOK = "a colossal dark violet crocodile-leviathan with huge pink blade fins, a jagged tail blade and a glowing magic circle above it"
build = make("leviamonxantibody", x=True)
