"""Duftmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the Royal Knight strategist, a slender leopard knight in brown armour with white plates, a long blonde mane, white feathered wings, a red sash, a rapier and a gold-ball tail.
35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from _digi import sized
from _duftmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a slender leopard knight in brown armour with white plates, a long blonde mane, white wings, a red sash, a rapier and a gold-ball tail"
build = make("duftmon")
