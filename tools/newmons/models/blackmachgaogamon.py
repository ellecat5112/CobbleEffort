"""Black Mach Gaogamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Mach Gaogamon's dark twin: a charcoal armoured wolf-man with a golden mane, steel chest
and shoulder plates, red gloves, a steel gauntlet and a jetpack of twin glowing boosters. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built by _gaogamon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _gaogamon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a charcoal armoured wolf-man with a golden mane, steel plates, red gloves, a steel gauntlet and a jetpack of "
        "twin boosters")
build = make("blackmachgaogamon", "perfect", black=True)
