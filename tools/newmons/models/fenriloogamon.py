"""Fenriloogamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the god-wolf, a huge prowling wolf in silver-and-navy plate with red eyes, a mane and tail of blazing blue
spirit-fire, a knotted rope round its neck and armoured paws with black hooked claws. 35 blocks tall.

Front is -z, y is up. 36 units tall; Ultimate stage.
"""
from _digi import sized
from _fenriloogamon import make

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a huge prowling wolf in silver-and-navy plate with red eyes, a mane and tail of blazing blue spirit-fire, a "
        "knotted rope round its neck and black hooked claws")
build = make("fenriloogamon")
