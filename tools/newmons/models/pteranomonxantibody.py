"""Pteranomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the navy stealth-jet pteranodon with swept delta wings, teal lights and twin blue thrusters. 15 blocks.
Built by _pteranomon.make(x=True).

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _pteranomon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a navy stealth-jet pteranodon with swept delta wings, teal running lights, twin booms and two blue jet thrusters"
build = make("pteranomonxantibody", x=True)
