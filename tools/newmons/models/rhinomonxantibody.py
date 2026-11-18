"""Rhinomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): a heavier bronze war rhino bristling with silver spikes, cyan-lit plates and a broadsword along its back.
15 blocks. Built by _rhinomon.make(x=True).

Front is -z, y is up. 32 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _rhinomon import make

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a heavy bronze war rhino bristling with silver spikes, cyan-lit plates and a great broadsword mounted along its back"
build = make("rhinomonxantibody", x=True)
