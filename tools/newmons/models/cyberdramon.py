"""Cyberdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a lean dark-grey cyborg dragon-man in ribbed armour with a horned visor, strapped muscled arms, huge clawed hands and tattered crimson wings. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

from _cyberdramon import make
from _digi import sized

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean dark-grey cyborg dragon-man in ribbed armour with a horned visor, strapped muscled arms, huge clawed hands and tattered crimson wings"

build = make("cyberdramon", x=False)
