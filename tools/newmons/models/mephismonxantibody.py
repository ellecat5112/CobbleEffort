"""Mephismon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the goat-skulled fallen angel as a dandy: a small top hat between its ram horns, long lilac hair, a blue tailcoat over a laced corset, grey puffed trousers, lilac goat legs, bat wings and a cane. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built by _mephismon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _mephismon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the goat-skulled fallen angel as a dandy: a small top hat between its ram horns, long lilac hair, a blue tailcoat over a laced corset, grey puffed trousers, lilac goat legs, bat wings and a cane"
build = make("mephismonxantibody", x=True)
