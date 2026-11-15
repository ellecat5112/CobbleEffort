"""Agumon Hakase (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): an Agumon in a mortarboard and a long white lab coat, holding a pointer.

Front is -z, y is up. 23 units tall; Child stage: 1 block.
"""
from __future__ import annotations

from _agumon import BLACK, ORANGE, build_agumon  # noqa: F401
from _digi import sized

HEIGHT = 23
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "biped"
K = 5
LOOK = "an Agumon in a mortarboard and a long white lab coat, holding a pointer"


def build():
    return build_agumon("agumonhakase", hakase=True)
