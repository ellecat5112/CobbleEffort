"""Dobermon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a lean,
long-legged black demon hound with tan markings, red eyes, swept-back ears, a steel spiked collar, red haunch slashes
and a ridge of short spines. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from _digi import sized
from _dobermon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a lean long-legged black demon hound with tan markings, red eyes, swept ears, a spiked collar and red slashes"
build = make("dobermon")
