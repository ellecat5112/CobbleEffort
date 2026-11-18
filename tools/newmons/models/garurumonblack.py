"""Garurumon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Garurumon's dark twin: black fur striped white, a mane of blade-like fur spikes, a long
curling tail and pink claws. Adult stage, 15 blocks tall.

Front is -z, y is up. 34 units tall. Built by _garurumon.make(look="black").
"""
from __future__ import annotations

from _digi import sized
from _garurumon import make

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a lean black wolf striped white with a mane of fur blades and a curling tail"
build = make("garurumonblack", "black")
