"""XV-mon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a muscular blue dragon-man of the V-mon line with a silver nose horn, a yellow V on
its brow, a great white X on its pale chest, small white bat wings and long silver claws. 15 blocks.

Front is -z, y is up. Adult stage. Built by _xvmon.make.
"""
from __future__ import annotations

from _digi import sized
from _xvmon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a muscular blue dragon-man with a silver nose horn, a white X on its chest, small white wings and silver claws"
build = make("xvmon", False)
