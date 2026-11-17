"""DORUgamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
beast dragon. A crouching four-legged dragon of dark navy fur striped with darker zigzags, a shaggy white chest, muzzle
and paws, pointed tan ears, a red eye, red hooked claws, a long striped tail and two great swept navy wings with white
undersides. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from _digi import sized
from _doru import gamon

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crouching navy fur dragon with zigzag stripes, a white chest, muzzle and paws, pointed ears, red claws and "
        "two great swept wings with white undersides")
build = gamon("dorugamon", "doru")
