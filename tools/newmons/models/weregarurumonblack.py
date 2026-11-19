"""Were Garurumon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a charcoal-furred wolf-man with a shaggy mane, camouflage trousers marked with a skull, a leather shoulder pad and spiked wrist bands. 25 blocks.

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
LOOK = "a charcoal-furred wolf-man with a shaggy mane, camouflage trousers marked with a skull, a leather shoulder pad and spiked wrist bands"
build = make("weregarurumonblack", "black")
