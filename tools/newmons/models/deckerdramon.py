"""Deckerdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a long, low crocodile war machine on caterpillar tracks with a gun deck, twin turrets, a missile pod and a tail launcher.
15 blocks tall.

Front is -z, y is up. 26 units tall; Adult stage.
"""
from _digi import sized
from _deckerdramon import make

HEIGHT = 26
SCALE, HITBOX = sized(15, HEIGHT, 3.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a long low crocodile war machine on caterpillar tracks with a slate gun deck, twin turrets, a missile pod and a tail launcher"
build = make("deckerdramon")
