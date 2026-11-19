"""Zubamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a small golden blade beast of sword-edged armour plates with a blade-crested head, red
eyes, a fanged jaw, a great ragged white mane and tail and a sword-tail. 1 block.

Front is -z, y is up. Child stage. Built by _zubamon.make.
"""
from __future__ import annotations

from _digi import sized
from _zubamon import make

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "a small golden blade beast with a blade crest, red eyes and a great ragged white mane and tail"
build = make("zubamon", False)
