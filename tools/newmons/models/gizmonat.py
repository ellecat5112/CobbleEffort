"""Gizmon: AT (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Gizumon war machine: a black sphere with a glowing yellow-red eye, its body a bundle of striped purple-and-green blade
fins hanging like a jellyfish, wires trailing beneath. Adult stage, 15 blocks tall.

Front is -z, y is up. 42 units tall. Built by _gizmon.make().
"""
from __future__ import annotations

from _digi import sized
from _gizmon import make

HEIGHT = 42
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "floater"
K = 3
LOOK = "a black sphere with a glowing eye above a bundle of striped purple-and-green blade fins hanging like a jellyfish"
build = make("gizmonat")
