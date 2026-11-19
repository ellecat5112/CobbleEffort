"""Trailmon of Darkness (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a living locomotive of the dark: a black segmented train with three glowing red eyes joined by green lines and rows of white lights. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 18
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living locomotive of the dark: a black segmented train with three glowing red eyes joined by green lines and rows of white lights"
build = make("trailmonofdarkness", "darkness")
