"""Chaosmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a slender knight in white, red and silver armour with long teal hair, a golden lion-head gauntlet and a long dragon-head lance-cannon. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _chaosmon import make
from _digi import sized

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slender knight in white, red and silver armour with long teal hair, a golden lion-head gauntlet and a long dragon-head lance-cannon"

build = make("chaosmon", valdur=False)
