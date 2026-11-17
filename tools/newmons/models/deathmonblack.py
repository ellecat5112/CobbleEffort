"""Deathmon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
Deathmon in charcoal black, its fiery wings and huge yellow eyes burning all the brighter. 35 blocks tall.

Front is -z, y is up. 44 units tall; Ultimate stage.
"""
from _deathmon import make
from _digi import sized

HEIGHT = 44
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a crouching charcoal-black demon with a horned helm, huge yellow eyes, fiery bat wings and bird-skull hands"
build = make("deathmonblack", black=True)
