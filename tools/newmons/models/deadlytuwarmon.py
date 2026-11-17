"""Deadly Tuwarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a towering gold war machine with a white star breastplate, a tall cone head with a red crest, white rolled-scroll
wings, a pickaxe staff, a lance-blade arm and huge axe-blade feet. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from _digi import sized
from _tuwar import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a towering gold war machine with a white star breastplate, a tall red-crested cone head, white scroll wings, a "
        "pickaxe staff and axe-blade feet")
build = make("deadlytuwarmon")
