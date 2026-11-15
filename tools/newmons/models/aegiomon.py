"""Aegiomon (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a young god-man with goat's horns and legs, white spiky hair, a red scarf, a black vest and one big white glove.

Front is -z, y is up. 36 units tall; 15 blocks.
"""
from __future__ import annotations

from _aegio import build_goat
from _digi import sized

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 1.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "a young god-man with goat's horns and legs, white spiky hair, a red scarf, a black vest and one big white glove"


def build():
    return build_goat("aegiomon", "aegiomon")
