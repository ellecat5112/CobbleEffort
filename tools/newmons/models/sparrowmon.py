"""Sparrowmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a sleek yellow jet-bird with a beaked cockpit, a green eye, swept wings, drill-tipped engine pods and clawed talons.
1 block(s). Built by _sparrowmon.make(ab=False). Child stage (no level on wikimon; by analogy).

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

from _digi import sized
from _sparrowmon import make

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a sleek yellow jet-bird with a beaked cockpit, a green eye, swept wings, drill-tipped engine pods and clawed talons"
build = make("sparrowmon", ab=False)
