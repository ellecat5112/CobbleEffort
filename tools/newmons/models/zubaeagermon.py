"""Zubaeagermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a lithe golden blade beast of sword-edged armour plates with a blade-crested head, red eyes,
a fanged jaw, and one huge curved golden blade for a tail trailing a blue arc. 15 blocks.

Front is -z, y is up. Adult stage. Built by _zubamon.make.
"""
from __future__ import annotations

from _digi import sized
from _zubamon import make

HEIGHT = 35
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "a lithe golden blade beast with a blade crest, red eyes and one huge curved golden blade tail"
build = make("zubaeagermon", True)
