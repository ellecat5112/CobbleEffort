"""Rosemon: Burst Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the radiant queen of flowers in a white bodysuit with a white rose hood, black gloves and boots, vast glowing pink petal wings and a thorned whip.
35 blocks. Built by _rosemon.make(look="burst").

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _rosemon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the radiant queen of flowers in a white bodysuit with a white rose hood, black gloves and boots, vast glowing pink petal wings and a thorned whip"
build = make("rosemonburstmode", look="burst")
