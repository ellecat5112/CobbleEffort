"""Sleipmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a six-legged crimson-armoured Royal Knight centaur with swirl shields, a horned horse-helm, a fiery mane, a crossbow and a halo of light.
35 blocks. Built by _sleipmon.make(look="base").

Front is -z, y is up. 72 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _sleipmon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a six-legged crimson-armoured Royal Knight centaur with swirl shields, a horned horse-helm, a fiery mane, a crossbow and a halo of light"
build = make("sleipmon", look="base")
