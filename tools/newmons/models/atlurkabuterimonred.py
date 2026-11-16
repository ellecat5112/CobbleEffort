"""Atlur Kabuterimon (Red) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): the crimson Atlur Kabuterimon, a hulking beetle-beast with a red carapace, a green
dome on its head, forked horns, a fanged maw over a skeletal chest plate and six jointed violet-clawed limbs.
25 blocks tall.

Front is -z, y is up. 46 units tall; Perfect stage. Built by atlurkabuterimonblue.make(red=True).
"""
from __future__ import annotations

from atlurkabuterimonblue import ANIM, HEIGHT, HITBOX, K, KIND, SCALE, make

LOOK = ("a hulking crimson beetle-beast with a green dome on its head, forked horns, a fanged maw over a skeletal "
        "chest plate and six jointed clawed limbs")
build, P = make("atlurkabuterimonred", red=True)
