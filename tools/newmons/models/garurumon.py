"""Garurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the lone wolf: a lean, powerful white wolf striped blue, with a mane of blade-like fur spikes,
a long curling striped tail, pink claws and a breath of blue fox-fire. Adult stage, 15 blocks tall.

Front is -z, y is up. 34 units tall. Built by _garurumon.make(look="base").
"""
from __future__ import annotations

from _digi import sized
from _garurumon import make

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a lean white wolf striped blue with a mane of fur blades, a curling tail and blue fox-fire"
build = make("garurumon", "base")
