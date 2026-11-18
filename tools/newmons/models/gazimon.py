"""Gazimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
sly little beast: a crouching lavender-grey creature with huge swept-back ears, long white sabre fangs, orange eyes
with dark marks, black claws and a fan-tipped tail bound with rings. Child stage, 1 block long.

Front is -z, y is up. 22 units tall. Built by _gazimon.make().
"""
from __future__ import annotations

from _digi import sized
from _gazimon import make

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a crouching lavender-grey beast with huge swept-back ears, long white sabre fangs and a fan-tipped tail"
build = make("gazimon")
