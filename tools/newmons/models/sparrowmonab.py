"""Sparrowmon AB (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Sparrowmon in heavier red-and-blue armour with a pair of big drill-cannons slung under its wings.
15 block(s). Built by _sparrowmon.make(ab=True). Adult stage (no level on wikimon; by analogy).

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

from _digi import sized
from _sparrowmon import make

HEIGHT = 20
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "Sparrowmon in heavier red-and-blue armour with a pair of big drill-cannons slung under its wings"
build = make("sparrowmonab", ab=True)
