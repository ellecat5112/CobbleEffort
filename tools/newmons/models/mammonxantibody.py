"""Mammon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Mammon awakened by the X-Antibody: a heavier dark-armoured shaggy mammoth with a dark blue eye-mask, a red saddle cloth, bronze wing-fins and stubby tusks. 25 blocks long. Built by _mammon.make(x=True).

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _mammon import make

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
LOOK = "a heavier dark-armoured shaggy mammoth with a dark blue eye-mask, a red saddle cloth, bronze wing-fins and stubby tusks"
build = make("mammonxantibody", x=True)
