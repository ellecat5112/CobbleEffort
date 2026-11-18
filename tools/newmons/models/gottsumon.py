"""Gottsumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
little pile of grey faceted rocks with two yellow eyes in a dark face hollow, rock-chunk ears and limbs of stacked
stones. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall. Built by _gottsumon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _gottsumon import make

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a little pile of grey faceted rocks with two yellow eyes and limbs of stacked stones"
build = make("gottsumon", x=False)
