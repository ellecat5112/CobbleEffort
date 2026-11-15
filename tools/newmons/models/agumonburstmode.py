"""Agumon: Burst Mode (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): an Agumon floating with its arms spread wide, wrapped in a translucent pink glow.

Front is -z, y is up. 23 units tall; Child stage: 1 block.
"""
from __future__ import annotations

from _agumon import BLACK, ORANGE, build_agumon  # noqa: F401
from _digi import sized

HEIGHT = 23
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "floater"
K = 5
LOOK = "an Agumon floating with its arms spread wide, wrapped in a translucent pink glow"


def build():
    return build_agumon("agumonburstmode", burst=True)
