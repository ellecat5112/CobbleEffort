"""Shoutmon X2 (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a chunky red-and-blue Xros robot with Shoutmon's head and V crest and big red fists. 15 blocks. Built by _shoutmon.mech.

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
LOOK = "a chunky red-and-blue Xros robot with Shoutmon's head and V crest and big red fists"
build = mech('shoutmonx2', robot=True)
