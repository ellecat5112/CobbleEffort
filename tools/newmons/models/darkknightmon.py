"""Dark Knightmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a tall black knight trimmed in gold with a horned crest, a great crescent shield-wing on its back and a long black-and-red lance. 25 blocks tall.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

from _darkknightmon import make
from _digi import sized

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a tall black knight trimmed in gold with a horned crest, a great crescent shield-wing on its back and a long black-and-red lance"

build = make("darkknightmon", x=False)
