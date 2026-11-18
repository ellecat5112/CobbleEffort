"""Meicrackmon: Vicious Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the cat warrior gone wild: a white mane, black armour on its forearms and shins, long red claws trailing red slashes, its ribbons looping overhead and its tail burning at the tip. 25 blocks tall.

Front is -z, y is up. 78 units tall (the ribbons included); Perfect stage. Built by _meicrackmon.make(vicious=True).
"""
from __future__ import annotations

from _digi import sized
from _meicrackmon import make

HEIGHT = 78
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the cat warrior gone wild: a white mane, black armour on its forearms and shins, long red claws trailing red slashes, its ribbons looping overhead and its tail burning at the tip"
build = make("meicrackmonviciousmode", vicious=True)
