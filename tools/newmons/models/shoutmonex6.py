"""Shoutmon EX6 (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a black-and-gold Xros giant with the Star Sword and a crested shield. 35 blocks. Built by _shoutmon.mech.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _shoutmon import mech, small  # noqa: F401

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a black-and-gold Xros giant with the Star Sword and a crested shield"
build = mech('shoutmonex6', colour='dark', drill=True, star_sword=True, shield=True)
