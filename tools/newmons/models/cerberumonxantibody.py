"""Cerberumon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a hulking dark-violet armoured beast bristling with huge blade spikes, long steel claws and a spiked tail. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

from _cerberumon import make
from _digi import sized

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a hulking dark-violet armoured beast bristling with huge blade spikes, long steel claws and a spiked tail"

build = make("cerberumonxantibody", "x")
