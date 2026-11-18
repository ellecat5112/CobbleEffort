"""Lopmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Lopmon awakened by the X-Antibody: a small brown rabbit with much longer tiger-marked ears ending in pink fingers, gold ornaments and fluffy cream shoulder puffs.
Child stage, 1 block tall. Built by _lopmon.make(x=True).

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

from _digi import sized
from _lopmon import make

HEIGHT = 18
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a small brown rabbit with much longer tiger-marked ears ending in pink fingers, gold ornaments and fluffy cream shoulder puffs"
build = make("lopmonxantibody", x=True)
