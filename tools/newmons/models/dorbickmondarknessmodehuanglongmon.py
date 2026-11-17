"""Dorbickmon Darkness Mode (Huanglongmon) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Dorbickmon in its darkness mode, riding a great golden dragon with a spiny back, a horned head and a long tail.
35 blocks tall.

Front is -z, y is up. 80 units tall; Ultimate stage.
"""
from _digi import sized
from _dorbickmon import make

HEIGHT = 80
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a crimson dragon-man riding a great golden dragon with a spiny back, horned head and long tail"
build = make("dorbickmondarknessmodehuanglongmon", "huang")
