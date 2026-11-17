"""Cerberumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a lean black underworld hound with steel-grey plates, red-lined joints, a snarling fanged head, a second head on its shoulder and long steel claws. 25 blocks tall.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

from _cerberumon import make
from _digi import sized

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a lean black underworld hound with steel-grey plates, red-lined joints, a snarling fanged head, a second head on its shoulder and long steel claws"

build = make("cerberumon", "base")
