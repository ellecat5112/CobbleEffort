"""Stingmon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a charcoal-black Stingmon with grey plates, red eyes, four translucent wings and arm spikes.
15 blocks. Built by _stingmon.make(black=True).

Front is -z, y is up. 70 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _stingmon import make

HEIGHT = 70
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a charcoal-black Stingmon with grey plates, red eyes, four translucent wings and arm spikes"
build = make("stingmonblack", black=True)
