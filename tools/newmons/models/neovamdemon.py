"""Neo Vamdemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the vampire king reborn: a towering insectoid figure of glossy violet-black armour bristling with curved blade spines, a narrow fanged mask with red eyes and long jointed legs. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _neovamdemon.make(mode="base").
"""
from __future__ import annotations

from _digi import sized
from _neovamdemon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the vampire king reborn: a towering insectoid figure of glossy violet-black armour bristling with curved blade spines, a narrow fanged mask with red eyes and long jointed legs"
build = make("neovamdemon", mode="base")
