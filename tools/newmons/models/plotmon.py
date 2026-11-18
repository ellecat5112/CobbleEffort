"""Plotmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
cream puppy with long floppy ears, big green eyes and a golden collar. 1 block. Built by _plotmon.make(x=False).

Front is -z, y is up. 20 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _plotmon import make

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a cream puppy with long floppy ears, big green eyes, blushing cheeks and a golden collar"
build = make("plotmon", x=False)
