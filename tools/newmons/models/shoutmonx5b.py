"""Shoutmon X5B (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the X5 knight on black exhaust-piped biker legs with the Star Sword and yellow jet. 35 blocks. Built by _shoutmon.mech.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _shoutmon import mech, small  # noqa: F401

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the X5 knight on black exhaust-piped biker legs with the Star Sword and yellow jet"
build = mech('shoutmonx5b', drill=True, star_sword=True, jet=True, biker=True)
