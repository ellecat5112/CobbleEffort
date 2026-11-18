"""Neo Vamdemon Darkness Mode (Metal Greymon) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Neo Vamdemon fused with a dark Metal Greymon: a coiled black serpent tail for a lower body, vast black wings and a fanged dragon maw in its chest. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _neovamdemon.make(mode="dragon").
"""
from __future__ import annotations

from _digi import sized
from _neovamdemon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Neo Vamdemon fused with a dark Metal Greymon: a coiled black serpent tail for a lower body, vast black wings and a fanged dragon maw in its chest"
build = make("neovamdemondarknessmodemetalgreymon", mode="dragon")
