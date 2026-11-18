"""Rasenmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
lion-beast knight in gunmetal armour with a white mane, a golden crest, a wheel of red-veined blade-quills and a
blazing sun-orb. 35 blocks. Built by _rasenmon.make(fury=False).

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _rasenmon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lion-beast knight in gunmetal armour with a white mane, a golden crest, a wheel of red-veined blade-quills and a sun-orb"
build = make("rasenmon", fury=False)
