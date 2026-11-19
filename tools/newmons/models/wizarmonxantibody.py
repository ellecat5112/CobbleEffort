"""Wizarmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Wizarmon changed by the X-Antibody: a huge tattered spiked mantle of navy and crimson, a gold mask,
armoured gold gauntlets, a sun-wheel staff and a crackle of blue sparks. 15 blocks.

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
LOOK = "a wizard with a huge tattered spiked navy-and-crimson mantle, a gold mask, gold gauntlets and a sun-wheel staff"
build = make("wizarmonxantibody", True)
