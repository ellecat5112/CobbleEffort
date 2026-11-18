"""Renamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
slender upright golden fox with a white ruff, purple yin-yang sleeve-gloves, a bushy white-tipped tail and a ring of
glowing leaves. 1 block. Built by _renamon.make(x=False).

Front is -z, y is up. 68 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _renamon import make

HEIGHT = 68
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a slender upright golden fox with a white ruff, purple yin-yang sleeve-gloves, a bushy white-tipped tail and a ring of leaves"
build = make("renamon", x=False)
