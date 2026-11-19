"""Taomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a tall fox onmyoji in a black-and-white fox-mask hood and a violet robe with huge
flared sleeves, a yin-yang mark on its chest, a golden fox tail, a giant calligraphy brush and red ofuda talismans
fluttering round it. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage. Built by _taomon.make.
"""
from __future__ import annotations

from _digi import sized
from _taomon import make

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall fox onmyoji in a fox-mask hood and a violet robe with huge sleeves, a giant brush and red ofuda talismans"
build = make("taomon", False)
