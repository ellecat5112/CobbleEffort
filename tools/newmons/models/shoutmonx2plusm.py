"""Shoutmon X2 Plus M (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the chunky red-and-blue X2 robot wielding a huge yellow-and-silver axe. 15 blocks. Built by _shoutmon.mech.

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
LOOK = "the chunky red-and-blue X2 robot wielding a huge yellow-and-silver axe"
build = mech('shoutmonx2plusm', robot=True, axe=True)
