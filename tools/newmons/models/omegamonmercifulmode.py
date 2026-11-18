"""Omegamon: Merciful Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Omegamon in Merciful Mode: silver-white plate trimmed ice-blue, great feathered wings of light and a blade of blue light from the dragon head. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _omegamon.make(look="merciful").
"""
from __future__ import annotations

from _digi import sized
from _omegamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Omegamon in Merciful Mode: silver-white plate trimmed ice-blue, great feathered wings of light and a blade of blue light from the dragon head"
build = make("omegamonmercifulmode", look="merciful")
