"""Dorbickmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the dragon general, an armoured dragon-man in layered crimson plates edged with black spikes, with round grey shoulder cannons, a long dragon head with black swept horns, huge clawed hands and feet and a spiked tail.
35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage.
"""
from _digi import sized
from _dorbickmon import make

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an armoured crimson dragon-man edged with black spikes, with grey shoulder cannons, black swept horns, huge claws and a spiked tail"
build = make("dorbickmon")
