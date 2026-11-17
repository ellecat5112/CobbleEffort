"""Chaosdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a hunched red machine dragon traced with dark grid lines, a fanged head with a nose horn, rounded shoulder pods, back cannons and huge grey crab-claw arms. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _chaosdramon import make
from _digi import sized

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hunched red machine dragon traced with dark grid lines, a fanged head with a nose horn, rounded shoulder pods, back cannons and huge grey crab-claw arms"

build = make("chaosdramon", x=False)
