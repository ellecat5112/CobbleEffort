"""Aegiochusmon: Green (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): Aegiochusmon in green leaf armour with two vine whips tipped with spiked pink seed-pods.

Front is -z, y is up. 36 units tall; 25 blocks.
"""
from __future__ import annotations

from _aegio import build_goat
from _digi import sized

HEIGHT = 36
SCALE, HITBOX = sized(25, HEIGHT, 1.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "Aegiochusmon in green leaf armour with two vine whips tipped with spiked pink seed-pods"


def build():
    return build_goat("aegiochusmongreen", "aegiochusmongreen")
