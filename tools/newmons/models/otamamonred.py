"""Otamamon (Red) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a round glossy red tadpole with a big smiling mouth of little teeth, round eyes, clawed forelimbs, webbed hind feet and a tall finned tail. 1 block tall.

Front is -z, y is up. 24 units tall; Child stage. Built by _otamamon.make(look="red").
"""
from __future__ import annotations

from _digi import sized
from _otamamon import make

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a round glossy red tadpole with a big smiling mouth of little teeth, round eyes, clawed forelimbs, webbed hind feet and a tall finned tail"
build = make("otamamonred", look="red")
