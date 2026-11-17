"""Black War Greymon "G" Erosion Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail
standard after the official art on wikimon.net): Black War Greymon eroded by a monstrous power: hulking violet-black
armour, tall glowing violet dorsal spines down its back and a long spined tail. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Built by _wargreymon.make("erosion").
"""
from __future__ import annotations

from _digi import sized
from _wargreymon import BASE, SHINY, make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ('Black War Greymon eroded by a monstrous power: hulking violet-black armour, tall glowing violet dorsal '
        'spines down its back and a long spined tail')
build = make("blackwargreymongerosionmode", "erosion")
