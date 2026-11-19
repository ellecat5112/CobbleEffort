"""Triceramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a hulking teal triceratops reared up on thick legs, with a spiked frill, a red-and-black
banded nose horn, two brow horns, an olive belly and huge ivory claws. 25 blocks.

Front is -z, y is up. Perfect stage. Built by _triceramon.make.
"""
from __future__ import annotations

from _digi import sized
from _triceramon import make

HEIGHT = 53
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking teal triceratops with a spiked frill, a red-and-black banded nose horn and huge ivory claws"
build = make("triceramon", False)
