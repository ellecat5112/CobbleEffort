"""Impmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the little devil: a purple imp with a white face, green eyes, a cocky fanged grin, a red bandana, a smiley badge, big
red gloves and a devil tail. Child stage, 1 block tall.

Front is -z, y is up. Built by _impmon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _impmon import make

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "a purple imp with a white face, green eyes, a red bandana, a smiley badge, big red gloves and a devil tail"
build = make("impmon", x=False)
