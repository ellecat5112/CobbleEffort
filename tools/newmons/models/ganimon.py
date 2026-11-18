"""Ganimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
grey-blue crab blotched with red, with a spiky shell, a little green-eyed fanged face, thin jointed legs and one great
pincer. Child stage, 1 block long.

Front is -z, y is up. 20 units tall. Built by _ganimon.make().
"""
from __future__ import annotations

from _digi import sized
from _ganimon import make

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 2.2)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a grey-blue red-blotched crab with a spiky shell, a green-eyed fanged face, thin legs and one great pincer"
build = make("ganimon")
