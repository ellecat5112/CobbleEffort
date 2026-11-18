"""Grademon (Vice) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Grademon's dark counterpart: navy-violet armour with red details, a long-horned helm, a
dark blue-black cape and one long curved blade. 25 blocks tall.

Front is -z, y is up. 76 units tall (the horns); Perfect stage. Built by _grademon.make(vice=True).
"""
from __future__ import annotations

from _digi import sized
from _grademon import make

HEIGHT = 76
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean navy-violet-armoured swordsman knight with a long-horned helm, a dark cape and one long curved blade"
build = make("grademonvice", vice=True)
