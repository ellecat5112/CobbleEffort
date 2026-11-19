"""Were Garurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a muscular white wolf-man striped blue, with a shaggy mane, ripped blue jeans marked with a skull, a leather shoulder pad and belts, spiked wrist bands and huge clawed feet. 25 blocks.

Front is -z, y is up. Perfect stage. Built by _weregarurumon.make.
"""
from __future__ import annotations

from _digi import sized
from _weregarurumon import make

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a muscular white wolf-man striped blue, with a shaggy mane, ripped blue jeans marked with a skull, a leather shoulder pad and belts, spiked wrist bands and huge clawed feet"
build = make("weregarurumon", "base")
