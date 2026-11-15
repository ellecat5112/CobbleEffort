"""Aegiochusmon: Holy (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): Aegiochusmon in white and gold holy armour with golden gear gauntlets, a halo and a sun of golden spikes behind it.

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
LOOK = "Aegiochusmon in white and gold holy armour with golden gear gauntlets, a halo and a sun of golden spikes behind it"


def build():
    return build_goat("aegiochusmonholy", "aegiochusmonholy")
