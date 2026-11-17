"""Demon Super Ultimate (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a lean black figure with a narrow horned head and a green waistband, wrapped in an enormous cloak of violet wings with great grasping claws at their tops.
45 blocks tall.

Front is -z, y is up. 96 units tall; Super Ultimate stage.
"""
from _digi import sized
from _demon import make

HEIGHT = 96
SCALE, HITBOX = sized(45, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean black horned figure with a green waistband wrapped in an enormous cloak of violet wings tipped with grasping claws"
build = make("demonsuperultimate", "super")
