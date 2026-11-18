"""Pucchiemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the little red fairy imp with heart-tipped antennae, red gloves and boots. 15 blocks. Built by
_pucchiemon.make(green=False).

Front is -z, y is up. 32 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _pucchiemon import make

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little white fairy imp in red with long bent antennae ending in heart arrowheads, big red gloves and chunky boots"
build = make("pucchiemon", green=False)
