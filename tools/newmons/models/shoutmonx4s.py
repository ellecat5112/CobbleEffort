"""Shoutmon X4S (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the X4 knight with the Star Sword and a long blue drill lance. 25 blocks. Built by _shoutmon.mech.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _shoutmon import mech, small  # noqa: F401

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the X4 knight with the Star Sword and a long blue drill lance"
build = mech('shoutmonx4s', drill=True, star_sword=True, lance=True)
