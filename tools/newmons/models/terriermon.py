"""Terriermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a small round cream bunny-dog with a single horn and two huge sweeping ears banded green, ending in three green fingers. 1 block.

Front is -z, y is up. Child stage. Built by _terriermon.make.
"""
from __future__ import annotations

from _digi import sized
from _terriermon import make

HEIGHT = 18
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a small round cream bunny-dog with a single horn and two huge sweeping ears banded green, ending in three green fingers"
build = make("terriermon", "base")
