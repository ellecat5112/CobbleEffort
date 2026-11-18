"""Monzaemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a giant yellow teddy bear with plush golden fur, a white belly with a crossed sticking plaster, round ears, a cream muzzle and stern closed eyes. 25 blocks tall.

Front is -z, y is up. 54 units tall; Perfect stage. Built by _monzaemon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _monzaemon import make

HEIGHT = 54
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a giant yellow teddy bear with plush golden fur, a white belly with a crossed sticking plaster, round ears, a cream muzzle and stern closed eyes"
build = make("monzaemon", x=False)
