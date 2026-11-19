"""Trailmon C-89 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a living steam locomotive: a navy engine with a whale-like white jaw, a red eye, smokestacks, gold piping and lettering, and red driving rods. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 22
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living steam locomotive: a navy engine with a whale-like white jaw, a red eye, smokestacks, gold piping and lettering, and red driving rods"
build = make("trailmonc89", "c89")
