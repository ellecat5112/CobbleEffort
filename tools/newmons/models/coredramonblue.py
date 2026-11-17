"""Coredramon (Blue) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a crouching blue scaly dragon with a cream belly, a fanged head crowned with red spikes, thick clawed limbs, a spiked tail and great bat wings. 15 blocks tall.

Front is -z, y is up. 46 units tall; Adult stage.
"""
from __future__ import annotations

from _coredramon import make
from _digi import sized

HEIGHT = 46
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a crouching blue scaly dragon with a cream belly, a fanged head crowned with red spikes, thick clawed limbs, a spiked tail and great bat wings"

build = make("coredramonblue", "blue")
