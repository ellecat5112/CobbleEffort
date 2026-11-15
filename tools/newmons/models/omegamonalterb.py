"""Omegamon Alter-B (Dark/Steel; a Digimon of the CobbleEffort: Digital crossover, built after the official art): the
knight gone dark: black armour seamed with glowing red, gold trim and talons, a horned crest with a red visor, a vast
tattered black cape, a red-black blade and a black lion-head shield with a golden cannon. 55 blocks tall; legendary.

Front is -z, y is up. 58 units tall; baseScale 15.4 (55 m).
"""
from __future__ import annotations

from _omega import build_knight

SCALE = 15.4
HITBOX = [1.8, 3.6]
KIND = "biped"
K = 3
HEIGHT = 58
ANIM = {"leg_amp": 10}
LOOK = ("the knight gone dark: black armour seamed with glowing red, gold trim and talons, a horned crest with a red "
        "visor, a vast tattered black cape, a red-black blade and a black lion-head shield with a golden cannon")


def build():
    return build_knight("omegamonalterb", "B")
