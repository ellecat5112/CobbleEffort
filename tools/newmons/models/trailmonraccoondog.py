"""Trailmon Raccoon Dog (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a living bullet train: a mint-green nose with a white lower jaw and a red-brown raccoon mask round its yellow eyes. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 18
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living bullet train: a mint-green nose with a white lower jaw and a red-brown raccoon mask round its yellow eyes"
build = make("trailmonraccoondog", "raccoon")
