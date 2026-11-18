"""Huanglongmon: Ruin Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): Huanglongmon fallen to ruin: dark violet armour, three heads on long necks and
cold blue flames pouring from its mouths and back. 35 blocks long.

Front is -z, y is up. Ultimate stage. Built by _huanglong.make(ruin=True).
"""
from __future__ import annotations

from _digi import sized
from _huanglong import make

HEIGHT = 38
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
LOOK = "a dark violet three-headed dragon with cold blue flames pouring from its mouths and back"
build = make("huanglongmonruinmode", ruin=True)
