"""Plotmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): a peach puppy with wide ears and a great rune-engraved golden ring round its body. 1 block. Built by
_plotmon.make(x=True).

Front is -z, y is up. 20 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _plotmon import make

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a peach puppy with wide floppy ears, big green eyes and a great rune-engraved golden ring round its body"
build = make("plotmonxantibody", x=True)
