"""Stingmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a lean wasp warrior in dark-green chitin with black plates, a red-eyed insect head, long antennae, four translucent wings and arm spikes.
15 blocks. Built by _stingmon.make(black=False).

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
LOOK = "a lean wasp warrior in dark-green chitin with black plates, a red-eyed insect head, long antennae, four translucent wings and arm spikes"
build = make("stingmon", black=False)
