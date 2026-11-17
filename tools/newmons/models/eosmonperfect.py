"""Eosmon (Perfect) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a slender crystal figure at the centre of four vast translucent hexagon-paned wings, with a crystal crown and a dangling chain of dark-blue crystal plates.
25 blocks tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from _digi import sized
from _eosmon import make

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a slender crystal figure in four vast hexagon-paned wings with a crystal crown and a dangling dark-blue crystal chain"
build = make("eosmonperfect", "perfect")
