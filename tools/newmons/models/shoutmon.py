"""Shoutmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a little red dragon with a white face, a big yellow toothy mouth, golden headphones, a red horn crest and a mic stand. 1 block. Built by _shoutmon.small.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _shoutmon import mech, small  # noqa: F401

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little red dragon with a white face, a big yellow toothy mouth, golden headphones, a red horn crest and a mic stand"
build = small('shoutmon', 'red')
