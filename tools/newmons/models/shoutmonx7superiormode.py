"""Shoutmon X7: Superior Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the gold-and-black Xros emperor with cream feather wings of light and red rings. 35 blocks. Built by _shoutmon.mech.

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
LOOK = "the gold-and-black Xros emperor with cream feather wings of light and red rings"
build = mech('shoutmonx7superiormode', colour='gold', drill=True, lance=True, light_wings=True)
