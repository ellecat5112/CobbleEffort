"""Aegiochusmon (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a red-skinned goat-legged god-man with tattoos, a fur mantle, long white hair, curled horns and white armoured thigh-guards.

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
LOOK = "a red-skinned goat-legged god-man with tattoos, a fur mantle, long white hair, curled horns and white armoured thigh-guards"


def build():
    return build_goat("aegiochusmon", "aegiochusmon")
