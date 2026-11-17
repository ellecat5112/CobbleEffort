"""Diablomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the rogue program: a wide flat swept purple shield head with a tiny orange-and-black face in the middle, from which hang long ragged olive-brown ribbon limbs ending in huge violet hands and feet with long red claws.
35 blocks tall.

Front is -z, y is up. 62 units tall; Ultimate stage.
"""
from _diablomon import make
from _digi import sized

HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a wide swept purple shield head with a tiny face, hanging from it long ragged ribbon limbs ending in huge violet hands and feet with red claws"
build = make("diablomon")
