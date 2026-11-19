"""Shoutmon X3GM (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the X3 knight with vast wings of golden flame. 25 blocks. Built by _shoutmon.mech.

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
LOOK = "the X3 knight with vast wings of golden flame"
build = mech('shoutmonx3gm', drill=True, flame_wings=True)
