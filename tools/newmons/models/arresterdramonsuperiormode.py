"""Arresterdramon: Superior Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): Arresterdramon at full power: gold-trimmed red-and-crimson armour on its chest
and shoulders, huge tattered yellow wings and a gold trident at the end of its tail. 25 blocks tall.

Front is -z, y is up. 62 units tall; Perfect stage (the generator's same-stage rule would add the levels).
Built by arresterdramon.make("superior").
"""
from __future__ import annotations

from _digi import sized
from arresterdramon import ANIM, BASE, HEIGHT, K, KIND, SHINY, make

SCALE, HITBOX = sized(25, HEIGHT, 1.8)
LOOK = ("Arresterdramon at full power: gold-trimmed crimson armour, huge tattered yellow wings and a gold trident tail")
build = make("arresterdramonsuperiormode", "superior")
