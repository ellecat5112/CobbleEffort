"""Plutomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
lord of the underworld: a gaunt knight in spiked black-and-gold armour with hound-skull pauldrons, a chain whip and a
vast tattered crimson cape flaring up like wings. 35 blocks. Built by _plutomon.make(fusion=False).

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _plutomon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a gaunt knight in spiked black-and-gold armour with hound-skull pauldrons, a chain whip and a vast tattered crimson cape"
build = make("plutomon", fusion=False)
