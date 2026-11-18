"""Gaioumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the dragon-man samurai: black-and-crimson lacquered armour, a horned dragon helm with a long
white mane, glowing teal eyes, two great curved blades and a tattered black cape. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _gaioumon.make().
"""
from __future__ import annotations

from _digi import sized
from _gaioumon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a dragon-man samurai in black-and-crimson armour with a long white mane, two great curved blades and a black cape"
build = make("gaioumon")
