"""Pucchiemon (Green) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the lime-green Pucchiemon. 15 blocks. Built by _pucchiemon.make(green=True).

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
LOOK = "a little white fairy imp in lime green with long bent antennae ending in heart arrowheads, big gloves and chunky boots"
build = make("pucchiemongreen", green=True)
