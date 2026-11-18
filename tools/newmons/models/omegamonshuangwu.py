"""Omegamon Shuang Wu (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Omegamon Shuang Wu: white plate trimmed violet, a crimson dragon gauntlet with its sword, the wolf cannon and a second great cannon over its shoulder. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _omegamon.make(look="shuangwu").
"""
from __future__ import annotations

from _digi import sized
from _omegamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Omegamon Shuang Wu: white plate trimmed violet, a crimson dragon gauntlet with its sword, the wolf cannon and a second great cannon over its shoulder"
build = make("omegamonshuangwu", look="shuangwu")
