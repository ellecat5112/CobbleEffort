"""Agumon (Black) (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a black X-Antibody Agumon scarred with red stripes, with long chrome claws.

Front is -z, y is up. 23 units tall; Child stage: 1 block.
"""
from __future__ import annotations

from _agumon import BLACK, ORANGE, build_agumon  # noqa: F401
from _digi import sized

HEIGHT = 23
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "biped"
K = 5
LOOK = "a black X-Antibody Agumon scarred with red stripes, with long chrome claws"


def build():
    return build_agumon("agumonblackxantibody", keys=BLACK, x_antibody=True)
