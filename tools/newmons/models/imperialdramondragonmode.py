"""Imperialdramon: Dragon Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): the ancient emperor dragon: a great four-legged dragon in black armour trimmed with
gold, gold talons, a white helm with a blue face, red-and-orange wings and a Positron Laser cannon on its back. 35
blocks tall.

Front is -z, y is up. Ultimate stage. Built by _imperial.make(mode="dragon", black=False).
"""
from __future__ import annotations

from _digi import sized
from _imperial import make

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
LOOK = "a great black-armoured four-legged dragon with gold talons, red wings, a white helm and a cannon on its back"
build = make("imperialdramondragonmode", mode="dragon", black=False)
