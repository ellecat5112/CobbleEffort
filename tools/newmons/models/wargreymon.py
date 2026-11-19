"""War Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the dragon warrior of courage: an orange dragon-man in gleaming gold Chrome Digizoid armour with a dragon-skull helm, a wild brown mane, three-clawed Dramon Destroyer gauntlets, the split Brave Shield on its back and a dinosaur tail. 35 blocks.

Front is -z, y is up. Ultimate stage. Built by _wargreymon.make("black"), recoloured.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_W = clone("_wargreymon", "wargreymon", base={'armour': (240, 196, 50), 'armour_dark': (170, 120, 20), 'armour_light': (255, 240, 160), 'gold': (210, 214, 226), 'gold_dark': (120, 124, 140), 'gold_light': (250, 250, 255), 'hair': (200, 110, 40), 'hair_dark': (140, 60, 20), 'skin': (240, 140, 50), 'skin_dark': (170, 80, 20)}, shiny={'armour': (60, 110, 200), 'armour_dark': (20, 50, 130), 'armour_light': (160, 200, 255)})
HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "an orange dragon-man in gold armour with a dragon-skull helm, a brown mane, three-clawed gauntlets and the split Brave Shield"
build = _W.make("wargreymon", "black")
