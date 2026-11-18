"""Galgomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
gun-toting rabbit: a stocky cream-and-green beast-man with huge floppy green ears, a red diamond on its brow, blue
jeans, and a gatling gun for each hand. Adult stage, 15 blocks tall.

Front is -z, y is up. 64 units tall. Built by _galgomon.make(black=False).
"""
from __future__ import annotations

from _digi import sized
from _galgomon import make

HEIGHT = 62
SCALE, HITBOX = sized(15, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a stocky cream-and-green rabbit beast-man with huge floppy ears, blue jeans and gatling guns for hands"
build = make("galgomon", "adult", black=False)
