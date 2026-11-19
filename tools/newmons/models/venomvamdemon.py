"""Venom Vamdemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Vamdemon's monstrous true form: a towering red demon with a ribbed chest streaked with violet,
a mane of wild blond hair, great black-and-red bat wings, huge shaggy furred legs with lilac claws and giant clawed
hands. 35 blocks.

Front is -z, y is up. Ultimate stage. Built by _venomvamdemon.make.
"""
from __future__ import annotations

from _digi import sized
from _venomvamdemon import make

HEIGHT = 76
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a towering red demon with a ribbed chest, wild blond hair, great bat wings, shaggy furred legs and giant clawed hands"
build = make("venomvamdemon", False)
