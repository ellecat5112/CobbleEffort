"""Chaosdramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a black-and-red machine dragon with two enormous grey bazooka cannons on its shoulders and huge crab-claw arms. 35 blocks tall.

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
LOOK = "a black-and-red machine dragon with two enormous grey bazooka cannons on its shoulders and huge crab-claw arms"

build = make("chaosdramonxantibody", x=True)
