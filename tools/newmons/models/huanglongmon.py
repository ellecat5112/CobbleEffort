"""Huanglongmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the yellow dragon, lord of the Four Holy Beasts: a great golden dragon armoured in gold
scale plates, antlered and whiskered, with a jade spine mane and twelve glowing orbs. 35 blocks long.

Front is -z, y is up. Ultimate stage. Built by _huanglong.make(ruin=False).
"""
from __future__ import annotations

from _digi import sized
from _huanglong import make

HEIGHT = 38
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
LOOK = "a great golden dragon in gold scale plates, antlered and whiskered, with a jade spine mane and twelve glowing orbs"
build = make("huanglongmon", ruin=False)
