"""Mugendramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the infinite machine dragon: a hunched colossus of chrome plates with a steel dinosaur head, red eyes, two great back cannons, huge three-clawed arms and a spined tail. 35 blocks tall.

Front is -z, y is up. 72 units tall (the cannons); Ultimate stage. Built by _mugendramon.make(mfs3=False).
"""
from __future__ import annotations

from _digi import sized
from _mugendramon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "the infinite machine dragon: a hunched colossus of chrome plates with a steel dinosaur head, red eyes, two great back cannons, huge three-clawed arms and a spined tail"
build = make("mugendramon", mfs3=False)
