"""Magnamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Magnamon awakened by the X-Antibody: a blue dragon-man in sharp faceted gold-orange armour edged with cyan crystals, a V-crested helm and a blue tail. 35 blocks tall. Built by _magnamon.make(x=True).

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _magnamon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a blue dragon-man in sharp faceted gold-orange armour edged with cyan crystals, a V-crested helm and a blue tail"
build = make("magnamonxantibody", x=True)
