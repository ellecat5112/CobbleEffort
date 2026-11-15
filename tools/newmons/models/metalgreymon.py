"""MetalGreymon (Steel/Dragon; a Digimon of the CobbleEffort: Digital crossover, built after the official art):
Greymon half rebuilt in steel: a steel helmet and horns, a steel chest plate with a glowing hatch, a huge steel Trident
Arm with three long claws, tattered purple wings and red spines down its neck, its tail still striped orange and blue.
25 blocks tall.

Front is -z, y is up. 42 units tall (the wings); baseScale 9.7 (25 m).
"""
from __future__ import annotations

from _greymon import build_body

SCALE = 9.7
HITBOX = [1.6, 2.6]
KIND = "biped"
K = 3
HEIGHT = 42
ANIM = {"leg_amp": 12}
LOOK = ("Greymon half rebuilt in steel: a steel helmet and horns, a steel chest plate with a glowing hatch, a huge steel "
        "Trident Arm with three long claws, tattered purple wings and red spines, its tail still striped")


def build():
    return build_body("metalgreymon", metal=True)
