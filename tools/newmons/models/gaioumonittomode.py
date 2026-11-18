"""Gaioumon: Itto Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Gaioumon wielding one blade: crimson armour trimmed in black and gold, a red ribbon
sash, sweeping horns, a long white mane and one huge serrated halberd-sword crackling with red lightning. 35 blocks.

Front is -z, y is up. 74 units tall; Ultimate stage. Built by _gaioumon.make(itto=True).
"""
from __future__ import annotations

from _digi import sized
from _gaioumon import make

HEIGHT = 74
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crimson-armoured dragon-man samurai with a red ribbon sash, sweeping horns, a long white mane and one huge "
        "serrated halberd-sword crackling with red lightning")
build = make("gaioumonittomode", itto=True)
