"""Sleipmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the X Royal Knight centaur in sharper crimson-and-black plate edged with cyan crystal, drawing a great crystal bow of cyan blades.
35 blocks. Built by _sleipmon.make(look="x").

Front is -z, y is up. 72 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _sleipmon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the X Royal Knight centaur in sharper crimson-and-black plate edged with cyan crystal, drawing a great crystal bow of cyan blades"
build = make("sleipmonxantibody", look="x")
