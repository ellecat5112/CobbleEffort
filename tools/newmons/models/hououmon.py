"""Hououmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the phoenix: a great golden bird with a hooked beak, a crest of flame feathers, vast golden wings and a
fan of long tail plumes tipped with red diamond eyes. 35 blocks tall.

Front is -z, y is up. 46 units tall; Ultimate stage. Built by _hououmon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _hououmon import make

HEIGHT = 46
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "floater"
K = 3
LOOK = "a great golden phoenix with a flame crest, vast golden wings and a fan of long tail plumes"
build = make("hououmon", x=False)
