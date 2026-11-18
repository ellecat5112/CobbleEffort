"""Rapidmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the sleek golden holy knight with long swept blade ears, cyan crystal edges and bladed gauntlets.
35 blocks. Built by _rapidarmor.make(x=True).

Front is -z, y is up. 76 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _rapidarmor import make

HEIGHT = 76
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a sleek golden holy knight with long swept blade ears, cyan crystal edges, bladed gauntlets and pointed greaves"
build = make("rapidmonxantibody", x=True)
