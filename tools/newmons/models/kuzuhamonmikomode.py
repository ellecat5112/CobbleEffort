"""Kuzuhamon: Miko Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Kuzuhamon as a shrine maiden, in a white kimono top and loose black hakama with long
black hair, a violet fox-eared cap and a silver ringed staff. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _kuzuha.make(miko=True).
"""
from __future__ import annotations

from _digi import sized
from _kuzuha import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a shrine maiden in a white kimono and black hakama with long black hair, a fox-eared cap and a silver ringed staff"
build = make("kuzuhamonmikomode", miko=True)
