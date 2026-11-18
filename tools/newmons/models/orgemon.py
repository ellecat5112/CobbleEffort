"""Orgemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a hunched muscular green ogre with warty skin, wild white hair, curved horns, a fanged roaring mouth, studded black bands, a red sash and a bone club. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage. Built by _orgemon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _orgemon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hunched muscular green ogre with warty skin, wild white hair, curved horns, a fanged roaring mouth, studded black bands, a red sash and a bone club"
build = make("orgemon", x=False)
