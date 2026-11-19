"""Skull Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): an undead dinosaur skeleton with a huge horned skull, green eye-lights, a red-glowing heart, raking claws and an organic missile on its back.
25 blocks. Built by _skullgreymon.make(erosion=False).

Front is -z, y is up. 52 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _skullgreymon import make

HEIGHT = 52
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an undead dinosaur skeleton with a huge horned skull, green eye-lights, a red-glowing heart, raking claws and an organic missile on its back"
build = make("skullgreymon", erosion=False)
