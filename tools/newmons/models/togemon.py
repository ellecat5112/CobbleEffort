"""Togemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a walking green cactus with three dark holes for a face, an orange tuft and big red
boxing gloves. 15 blocks.

Front is -z, y is up. Adult stage. Built by _togemon.make.
"""
from __future__ import annotations

from _digi import sized
from _togemon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a walking green cactus with a hole face, an orange tuft and big red boxing gloves"
build = make("togemon", False)
