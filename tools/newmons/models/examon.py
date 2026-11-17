"""Examon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the dragon Royal Knight, a vast crimson dragon with a long armoured neck, spined back, enormous ribbed red membrane wings, a silver knight's head and the great lance Ambitious.
35 blocks tall.

Front is -z, y is up. 44 units tall; Ultimate stage.
"""
from _digi import sized
from _examon import make

HEIGHT = 44
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a vast crimson dragon with a long armoured neck, spined back, enormous ribbed red wings, a silver knight head and a great lance"
build = make("examon")
