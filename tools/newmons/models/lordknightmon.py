"""Lord Knightmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the rose Royal Knight: a slender knight in rose-pink armour with gold trim, a crested helm, long golden ribbons, a large golden oval shield with a blue gem and long pointed greaves. 35 blocks tall. Built by _lordknightmon.make(x=False).

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _lordknightmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slender knight in rose-pink armour with gold trim, a crested helm, long golden ribbons, a large golden oval shield with a blue gem and long pointed greaves"
build = make("lordknightmon", x=False)
