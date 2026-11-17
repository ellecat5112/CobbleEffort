"""Black War Greymon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): Black War Greymon awakened by the X-Antibody: black armour with glowing red
seams, the Brave Shield opened into great blade-wings, three-clawed gauntlets and a golden mane. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Built by _wargreymon.make("blackx").
"""
from __future__ import annotations

from _digi import sized
from _wargreymon import BASE, SHINY, make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ('Black War Greymon awakened by the X-Antibody: black armour with glowing red seams, the Brave Shield '
        'opened into great blade-wings, three-clawed gauntlets and a golden mane')
build = make("blackwargreymonxantibody", "blackx")
