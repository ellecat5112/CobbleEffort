"""Nefertimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of light: a white sphinx with a woman's face behind a golden pharaoh headdress, silver-and-gold armour set with red gems, great white wings and a violet-tufted tail. 15 blocks long.

Front is -z, y is up. 36 units tall; Adult (Armor) stage. Built by _nefertimon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _nefertimon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the Armor Digimon of light: a white sphinx with a woman's face behind a golden pharaoh headdress, silver-and-gold armour set with red gems, great white wings and a violet-tufted tail"
build = make("nefertimon", x=False)
