"""Wizarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the wandering wizard: a broad blue hat with a skull, a high collar hiding all but its
green eyes, yellow-and-red striped clothes, a ragged star-lined purple cape, a sun-wheel staff and a glowing spell
orb. 15 blocks.

Front is -z, y is up. Adult stage. Built by _wizarmon.make.
"""
from __future__ import annotations

from _digi import sized
from _wizarmon import make

HEIGHT = 68
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a wandering wizard with a broad blue skull hat, striped clothes, a star-lined purple cape, a sun-wheel staff and a spell orb"
build = make("wizarmon", False)
