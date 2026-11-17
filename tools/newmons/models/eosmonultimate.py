"""Eosmon (Ultimate) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a gold-and-blue figure in a bell of blue feathers, crowned with golden spikes, before a great fan of iridescent rainbow crystal blades, with a violet orb beneath.
35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from _digi import sized
from _eosmon import make

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a gold-and-blue figure in a bell of blue feathers before a fan of rainbow crystal blades, with a violet orb beneath"
build = make("eosmonultimate", "ultimate")
