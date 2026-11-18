"""Mad Leomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Leomon turned undead: a hunched violet-grey lion-man with stitched patchy skin, a wild black mane,
bone horns, a fanged snarl and banded black armour on its forearms and shins. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage. Built by _madleomon.make(mode="base").
"""
from __future__ import annotations

from _digi import sized
from _madleomon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hunched violet-grey lion-man with stitched patchy skin, a wild black mane, bone horns, a fanged snarl and banded black armour on its forearms and shins"
build = make("madleomon", mode="base")
