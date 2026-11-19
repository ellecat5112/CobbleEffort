"""Skull Greymon: "G" Erosion Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Skull Greymon overgrown with a wild mane of grey bone spines and a sick violet glow.
25 blocks. Built by _skullgreymon.make(erosion=True).

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
LOOK = "Skull Greymon overgrown with a wild mane of grey bone spines and a sick violet glow"
build = make("skullgreymongerosionmode", erosion=True)
