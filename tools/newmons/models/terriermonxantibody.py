"""Terriermon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): Terriermon changed by the X-Antibody: much longer green tiger-striped ears with a gold ornament and a green gem, and a shaggy golden mane. 1 block.

Front is -z, y is up. Child stage. Built by _terriermon.make.
"""
from __future__ import annotations

from _digi import sized
from _terriermon import make

HEIGHT = 18
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "Terriermon changed by the X-Antibody: much longer green tiger-striped ears with a gold ornament and a green gem, and a shaggy golden mane"
build = make("terriermonxantibody", "x")
