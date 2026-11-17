"""Erlangmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the god of the three-pointed spear, a tall warrior in silver and violet armour with a horned gold crest, a long robe, a gold trident and a spectral dragon-hound spirit behind it.
35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from _digi import sized
from _erlangmon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a tall silver-and-violet armoured warrior with a horned gold crest, a long robe, a gold trident and a spectral hound spirit"
build = make("erlangmon")
