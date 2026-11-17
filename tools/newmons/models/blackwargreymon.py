"""Black War Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the dark twin of War Greymon: black Chrome Digizoid armour with gold trim, a dragon-
skull helm, a golden mane, three-clawed gauntlets, a black Brave Shield on its back and a dinosaur tail. 35 blocks
tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Built by _wargreymon.make("black").
"""
from __future__ import annotations

from _digi import sized
from _wargreymon import BASE, SHINY, make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ('the dark twin of War Greymon: black Chrome Digizoid armour with gold trim, a dragon-skull helm, a golden '
        'mane, three-clawed gauntlets, a black Brave Shield on its back and a dinosaur tail')
build = make("blackwargreymon", "black")
