"""Imperialdramon: Dragon Mode (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail
standard after the official art on wikimon.net): the black emperor dragon: Dragon Mode in darker armour with a silver
helm, red eyes and tattered crimson wings. 35 blocks tall.

Front is -z, y is up. Ultimate stage. Built by _imperial.make(mode="dragon", black=True).
"""
from __future__ import annotations

from _digi import sized
from _imperial import make

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
LOOK = "a great dark four-legged dragon with gold talons, tattered crimson wings, a silver helm and a cannon on its back"
build = make("imperialdramondragonmodeblack", mode="dragon", black=True)
