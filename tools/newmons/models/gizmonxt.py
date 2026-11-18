"""Gizmon: XT (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
upgraded Gizumon: a violet sphere on a violet torso with a white ringed waist, great purple-and-green swept blade
wings, a small head pod with a red eye and thin cabled legs on white pod feet. Perfect stage, 25 blocks tall.

Front is -z, y is up. 40 units tall. Built by _gizmon.make(xt=True).
"""
from __future__ import annotations

from _digi import sized
from _gizmon import make

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a violet sphere-bodied war machine with great purple-and-green blade wings and thin cabled legs"
build = make("gizmonxt", xt=True)
