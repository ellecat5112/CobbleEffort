"""Keramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Keramon awakened by the X-Antibody: a bigger dark-veined head covered in red-ringed eyes, a gaping mouth, a crown of spikes and longer tangled tendrils.
Child stage, 1 block tall. Built by _keramon.make(x=True).

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

from _digi import sized
from _keramon import make

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a dark-veined data bug with many red-ringed eyes, a gaping mouth, a crown of spikes and tangled tendrils"
build = make("keramonxantibody", x=True)
