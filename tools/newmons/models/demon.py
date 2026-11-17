"""Demon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the Demon Lord of Wrath, a tall fallen angel in a fur-trimmed dark-red coat with curling silver horns, white hair, a gold pentagram badge, red claws and huge violet bat wings.
35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from _digi import sized
from _demon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall fallen angel in a fur-trimmed dark-red coat with curling silver horns, white hair, red claws and huge violet bat wings"
build = make("demon")
