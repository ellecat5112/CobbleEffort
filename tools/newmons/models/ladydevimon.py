"""Lady Devimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the fallen angel lady: a tall figure fully covered in a black leather bodysuit bound with silver chains, a hood-mask with red eyes, long white hair, a tattered black cape and a great clawed arm. 25 blocks tall. Built by _ladydevimon.make(x=False), fully clothed as drawn.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _ladydevimon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall figure fully covered in a black leather bodysuit bound with silver chains, a hood-mask with red eyes, long white hair, a tattered black cape and a great clawed arm"
build = make("ladydevimon", x=False)
