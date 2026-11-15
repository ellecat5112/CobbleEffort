"""Greymon (Fire/Dragon; a Digimon of the CobbleEffort: Digital crossover, built after the official art): a hunched
orange tyrant with blue tiger stripes, a brown skull helmet with a nose horn and two side horns, an open jaw full of
white fangs, big white claws and a long striped tail. 15 blocks tall.

Front is -z, y is up. 41 units tall; baseScale 6.0 (15 m).
"""
from __future__ import annotations

from _greymon import build_body

SCALE = 6.0
HITBOX = [1.6, 2.55]
KIND = "biped"
K = 3
HEIGHT = 41
ANIM = {"leg_amp": 14}
LOOK = ("a hunched orange tyrant with blue tiger stripes, a brown skull helmet with a nose horn and two side horns, an "
        "open jaw full of white fangs, big white claws and a long striped tail")


def build():
    return build_body("greymon", metal=False)
