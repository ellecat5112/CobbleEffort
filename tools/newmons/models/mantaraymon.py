"""Mantaraymon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the Armor Digimon manta: a broad violet manta ray with pointed wing-fins, tall dorsal spikes, pale stripes, a golden crest between red eyes and a long whip tail.
15 blocks wide. Built by _mantaraymon.make(x=False).

Front is -z, y is up. 20 units tall; Adult stage (Armor).
"""
from __future__ import annotations

from _digi import sized
from _mantaraymon import make

HEIGHT = 20
SCALE, HITBOX = sized(15, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a broad violet manta ray with pointed wing-fins, tall dorsal spikes, pale stripes, a golden crest between red eyes and a long whip tail"
build = make("mantaraymon", x=False)
