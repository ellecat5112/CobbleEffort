"""Vamdemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the vampire lord: a tall gaunt figure in a navy suit with gold buttons, a huge black cape
lined in red with a high collar, a red half-mask with gold horns, red clawed gloves, skull-toed boots and circling
bats. 25 blocks.

Front is -z, y is up. Perfect stage. Built by _vamdemon.make.
"""
from __future__ import annotations

from _digi import sized
from _vamdemon import make

HEIGHT = 63
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall vampire lord in a navy suit with a red-lined black cape, a red horned half-mask and circling bats"
build = make("vamdemon", False)
