"""Darkness Bagramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the dark emperor: a gaunt figure in black-and-gold armour with a horned crown, a skeletal red-clawed arm, ragged black wings and an enormous deep-blue cape. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _darknessbagramon import make
from _digi import sized

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the dark emperor: a gaunt figure in black-and-gold armour with a horned crown, a skeletal red-clawed arm, ragged black wings and an enormous deep-blue cape"

build = make("darknessbagramon", dk=False)
