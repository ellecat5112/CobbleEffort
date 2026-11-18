"""Knightmon Wise Sword Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): Knightmon in its Wise Sword Mode, the same silver plate knight with a yellow scarf,
a brown cloak, a great golden blade-staff with a jewelled pommel and a curved sabre at its side. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect (no level on wikimon) stage. Built by _knightmon.make(wise=True).
"""
from __future__ import annotations

from _digi import sized
from _knightmon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a silver plate knight with a yellow scarf, a brown cloak, a golden blade-staff and a curved sabre"
build = make("knightmonwiseswordmode", wise=True)
