"""Yuki Agumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Agumon of the snowfields: the familiar little dinosaur in frosty pale blue with a white belly,
blue eyes, a toothy grin and white claws. 1 block.

Front is -z, y is up. Child stage. The Agumon body (_agumon.build_agumon) in snow colours.
"""
from __future__ import annotations

from _agumon import build_agumon
from _digi import sized

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "biped"
K = 5
ANIM = {"leg_amp": 12}
LOOK = "a little frosty pale-blue dinosaur with a white belly, blue eyes, a toothy grin and white claws"
_SNOW = {"hide": "snow", "dark": "snow_dark", "belly": "snow_belly", "stripe": "stripe"}


def build():
    return build_agumon("yukiagumon", keys=_SNOW)
