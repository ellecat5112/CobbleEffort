"""Shoutmon X4 (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the X3 knight wielding the red serrated Star Sword with its gold star guard. 15 blocks. Built by _shoutmon.mech.

Front is -z, y is up. 66 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _shoutmon import mech, small  # noqa: F401

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the X3 knight wielding the red serrated Star Sword with its gold star guard"
build = mech('shoutmonx4', drill=True, star_sword=True)
