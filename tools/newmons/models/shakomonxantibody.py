"""Shakomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a huge lilac shell like a helmet with magenta flame marks and spikes, a big green frog-like face peering out and a steel clamp.
1 block. Built by _shakomon.make(x=True).

Front is -z, y is up. 20 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _shakomon import make

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "floater"
K = 3
LOOK = "a huge lilac shell like a helmet with magenta flame marks and spikes, a big green frog-like face peering out and a steel clamp"
build = make("shakomonxantibody", x=True)
