"""Omegamon Alter-S (Steel/Fighting; a Digimon of the CobbleEffort: Digital crossover, built after the official art): a
towering white knight trimmed in gold on long legs with golden talons, spiked gold pauldrons, a horned crest with a red
visor, a tattered black cape, a long golden sword on one arm and a red lion-head shield with a great cannon on the
other. 45 blocks tall.

Front is -z, y is up. 58 units tall; baseScale 12.6 (45 m).
"""
from __future__ import annotations

from _omega import build_knight

SCALE = 12.6
HITBOX = [1.8, 3.6]
KIND = "biped"
K = 3
HEIGHT = 58
ANIM = {"leg_amp": 10}
LOOK = ("a towering white knight trimmed in gold: long legs with golden talons, spiked gold pauldrons, a horned crest "
        "with a red visor, a tattered black cape, a long golden sword and a red lion-head shield with a great cannon")


def build():
    return build_knight("omegamonalters", "S")
