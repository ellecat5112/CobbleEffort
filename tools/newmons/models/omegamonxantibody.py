"""Omegamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Omegamon changed by the X-Antibody: blue-violet plate trimmed gold, more gold spikes, a rune-engraved sword and a red-lined cape. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _omegamon.make(look="x").
"""
from __future__ import annotations

from _digi import sized
from _omegamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Omegamon changed by the X-Antibody: blue-violet plate trimmed gold, more gold spikes, a rune-engraved sword and a red-lined cape"
build = make("omegamonxantibody", look="x")
