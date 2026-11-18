"""Jyureimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
haunted forest tree, a gnarled trunk with a scowling face of hollow knots and glowing yellow eyes, vine garlands, a
great round crown of dark leaves dotted with red berries and a tangle of roots. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage. Built by _jyureimon.make(xmas=False).
"""
from __future__ import annotations

from _digi import sized
from _jyureimon import make

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 0}
LOOK = "a gnarled haunted tree with a scowling knot face, glowing eyes, vine garlands and a round berry-dotted crown"
build = make("jyureimon", xmas=False)
