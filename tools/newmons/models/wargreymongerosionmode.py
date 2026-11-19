"""War Greymon: "G" Erosion Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): War Greymon eaten away by the "G" erosion: corrupted violet-black armour streaked with sickly yellow, tall glowing magenta dorsal spines down its back and a long spined tail. 35 blocks.

Front is -z, y is up. Ultimate stage. Built by _wargreymon.make("erosion"), recoloured.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_W = clone("_wargreymon", "wargreymongerosionmode", base={'gold': (220, 200, 60), 'gold_dark': (150, 130, 20), 'hair': (190, 80, 180), 'hair_dark': (120, 30, 110), 'skin': (230, 130, 60), 'skin_dark': (160, 70, 20), 'violet': (240, 80, 220), 'violet_dark': (150, 30, 140)}, shiny={})
HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "War Greymon corrupted: violet-black armour streaked yellow, glowing magenta dorsal spines and a spined tail"
build = _W.make("wargreymongerosionmode", "erosion")
