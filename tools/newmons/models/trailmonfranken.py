"""Trailmon Franken (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a living diesel locomotive: a maroon train with a grey grille face, green eyes on its brow and an orange lamp. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 20
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living diesel locomotive: a maroon train with a grey grille face, green eyes on its brow and an orange lamp"
build = make("trailmonfranken", "franken")
