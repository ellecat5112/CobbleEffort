"""Duftmon: Leopard Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Duftmon as a crouching armoured leopard with a blonde mane, blue shoulder spikes, white wings, red claws and the gold-ball tail.
35 blocks tall.

Front is -z, y is up. 32 units tall; Ultimate stage.
"""
from _digi import sized
from _duftmon import make

HEIGHT = 32
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a crouching brown-armoured leopard with a blonde mane, blue shoulder spikes, white wings, red claws and a gold-ball tail"
build = make("duftmonleopardmode", "leopard")
