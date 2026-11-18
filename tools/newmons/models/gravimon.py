"""Gravimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
gaunt skeletal white giant with a long ribbed spine for a waist, a tattered black shroud of hair streaming from its
head, huge hanging clawed hands and long dark cables looping round it ending in brass plugs. 25 blocks tall.

Front is -z, y is up. 66 units tall; Perfect stage. Built by _gravimon.make(dark=False).
"""
from __future__ import annotations

from _digi import sized
from _gravimon import make

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a gaunt skeletal white giant with a ribbed spine waist, streaming black hair, huge clawed hands and looping cables"
build = make("gravimon", dark=False)
