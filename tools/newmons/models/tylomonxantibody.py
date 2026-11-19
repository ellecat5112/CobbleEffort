"""Tylomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Tylomon changed by the X-Antibody: heavier steel-blue armour with gold trim and glowing cyan
seams, a serrated spine of blades and a crested tail fin. 15 blocks.

Front is -z, y is up. Adult stage (Armor). Built by _tylomon.make.
"""
from __future__ import annotations

from _digi import sized
from _tylomon import make

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a steel-blue armoured shark-like sea reptile with gold trim, cyan seams and a serrated spine of blades"
build = make("tylomonxantibody", True)
