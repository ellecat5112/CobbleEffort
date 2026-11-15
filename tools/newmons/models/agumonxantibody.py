"""Agumon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): an X-Antibody Agumon: a fiercer little dinosaur with long chrome claws and a striped tail.

Front is -z, y is up. 23 units tall; Child stage: 1 block.
"""
from __future__ import annotations

from _agumon import BLACK, ORANGE, build_agumon  # noqa: F401
from _digi import sized

HEIGHT = 23
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "biped"
K = 5
LOOK = "an X-Antibody Agumon: a fiercer little dinosaur with long chrome claws and a striped tail"


def build():
    return build_agumon("agumonxantibody", x_antibody=True)
