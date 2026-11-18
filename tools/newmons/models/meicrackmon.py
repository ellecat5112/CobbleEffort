"""Meicrackmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a slender cat warrior in a golden-orange fur bodysuit striped black with a great white fluffy collar, ribbon ears looping into a heart over its head, glowing pink orbs at its paws and dark boots. 25 blocks tall.

Front is -z, y is up. 78 units tall (the ribbons included); Perfect stage. Built by _meicrackmon.make(vicious=False).
"""
from __future__ import annotations

from _digi import sized
from _meicrackmon import make

HEIGHT = 78
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a slender cat warrior in a golden-orange fur bodysuit striped black with a great white fluffy collar, ribbon ears looping into a heart over its head, glowing pink orbs at its paws and dark boots"
build = make("meicrackmon", vicious=False)
