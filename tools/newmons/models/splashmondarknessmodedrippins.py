"""Splashmon Darkness Mode (Drippins) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Splashmon grown into a hulking pale-blue giant in a gold-banded white bodysuit with flowing lilac hair.
25 blocks. Built by _splashmon.make(mode="drippins").

Front is -z, y is up. 70 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _splashmon import make

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Splashmon grown into a hulking pale-blue giant in a gold-banded white bodysuit with flowing lilac hair"
build = make("splashmondarknessmodedrippins", mode="drippins")
