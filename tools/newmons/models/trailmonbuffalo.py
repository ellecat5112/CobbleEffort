"""Trailmon Buffalo (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a living locomotive: a slate-purple train with green eyes, two great golden horns and a spiked snow-plough. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 21
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living locomotive: a slate-purple train with green eyes, two great golden horns and a spiked snow-plough"
build = make("trailmonbuffalo", "buffalo")
