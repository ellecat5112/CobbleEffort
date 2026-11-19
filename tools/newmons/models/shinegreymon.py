"""Shine Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a light dragon-man in white armour banded red with a golden dragon helm, eight red blade-wings tipped blue and a golden sun-wheel.
35 blocks. Built by _shinegreymon.make(look="base").

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _shinegreymon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a light dragon-man in white armour banded red with a golden dragon helm, eight red blade-wings tipped blue and a golden sun-wheel"
build = make("shinegreymon", look="base")
