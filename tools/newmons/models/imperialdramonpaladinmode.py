"""Imperialdramon: Paladin Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): the emperor dragon as a holy knight: white-and-silver armour trimmed with
gold, white wings, a red cape and the long Omega Blade. 35 blocks tall.

Front is -z, y is up. Ultimate stage. Built by _imperial.make(mode="paladin", black=False).
"""
from __future__ import annotations

from _digi import sized
from _imperial import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an upright white-and-silver holy knight dragon with white wings, a red cape and a long sword"
build = make("imperialdramonpaladinmode", mode="paladin", black=False)
