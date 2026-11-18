"""Prince Mamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the little prince of the Mamemon: a round yellow face with a smug grin, a jewelled crown, a royal-blue
suit and a great red cape trimmed in ermine. 35 blocks. Built by _princemamemon.make(x=False).

Front is -z, y is up. 34 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _princemamemon import make

HEIGHT = 34
SCALE, HITBOX = sized(35, HEIGHT, 2.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a round yellow face with a smug grin and spiral cheeks, a jewelled crown, a royal-blue suit and a great red ermine-trimmed cape"
build = make("princemamemon", x=False)
