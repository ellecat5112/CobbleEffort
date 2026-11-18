"""Gankoomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Royal Knight who fights as a man: a lean warrior in a black red-seamed bodysuit with spiky
red hair and a long white tattered coat, and towering behind him his golden spirit Hinukamuy, a translucent maned
giant with flaming fists. 35 blocks tall.

Front is -z, y is up. 96 units tall (the spirit included); Ultimate stage. Built by _gankoomon.make().
"""
from __future__ import annotations

from _digi import sized
from _gankoomon import make

HEIGHT = 96
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a lean warrior in a black bodysuit with spiky red hair and a white coat, his towering translucent golden spirit "
        "with flaming fists behind him")
build = make("gankoomon")
