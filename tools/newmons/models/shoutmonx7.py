"""Shoutmon X7 (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a gold-and-black Xros emperor with a jet arm and a long drill lance. 35 blocks. Built by _shoutmon.mech.

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
LOOK = "a gold-and-black Xros emperor with a jet arm and a long drill lance"
build = mech('shoutmonx7', colour='gold', drill=True, jet=True, lance=True)
