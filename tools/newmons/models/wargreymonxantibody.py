"""War Greymon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): War Greymon changed by the X-Antibody: orange-and-blue armour with glowing cyan seams, the Brave Shield opened into great blade-wings, three-clawed gauntlets and a fiery mane. 35 blocks.

Front is -z, y is up. Ultimate stage. Built by _wargreymon.make("blackx"), recoloured.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_W = clone("_wargreymon", "wargreymonxantibody", base={'armour': (240, 130, 40), 'armour_dark': (60, 70, 170), 'armour_light': (255, 210, 120), 'gold': (80, 100, 210), 'gold_dark': (30, 40, 120), 'gold_light': (170, 190, 255), 'hair': (240, 140, 40), 'hair_dark': (180, 70, 20), 'skin': (240, 140, 50), 'skin_dark': (170, 80, 20), 'red': (120, 230, 255)}, shiny={'armour': (180, 190, 210), 'armour_dark': (90, 100, 130)})
HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "War Greymon with orange-and-blue armour, glowing cyan seams and the Brave Shield opened into blade-wings"
build = _W.make("wargreymonxantibody", "blackx")
