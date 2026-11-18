"""Gururumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a wild cousin of Garurumon: a lean white wolf striped in deep blue with a mane of blade-like fur
spikes, red eyes, violet claws and a long curling striped tail. Adult stage, 15 blocks tall.

Front is -z, y is up. 34 units tall. Built by _garurumon.make(look="gururu").
"""
from __future__ import annotations

from _digi import sized
from _garurumon import make

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a lean white wolf striped deep blue with a mane of fur blades, red eyes, violet claws and a curling tail"
build = make("gururumon", "gururu")
