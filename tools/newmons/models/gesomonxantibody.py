"""Gesomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Gesomon awakened by the X-Antibody: a squat pale-blue squid with a tiger-striped mantle, gold rings in
its fins, a grinning toothy maw and tentacle arms ending in their own snapping mouths. Adult stage, 15 blocks tall.

Front is -z, y is up. 36 units tall. Built by _gesomon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _gesomon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = "a squat pale-blue tiger-striped squid with a toothy grin and tentacle arms ending in mouths"
build = make("gesomonxantibody", x=True)
