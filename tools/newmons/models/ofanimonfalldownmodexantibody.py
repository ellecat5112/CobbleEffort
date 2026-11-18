"""Ofanimon: Falldown Mode (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the fallen Ofanimon changed by the X-Antibody: black-teal armour, red tendrils and three spiked golden rings orbiting her. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built covered (full armour). Built by _ofanimon.make(look="falldownx").
"""
from __future__ import annotations

from _digi import sized
from _ofanimon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "the fallen Ofanimon changed by the X-Antibody: black-teal armour, red tendrils and three spiked golden rings orbiting her"
build = make("ofanimonfalldownmodexantibody", look="falldownx")
