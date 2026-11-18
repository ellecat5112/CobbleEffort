"""Impmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Impmon awakened by the X-Antibody: a long-limbed imp in a tall wizard hat with an X visor, a tattered red
cape-wing, and blue fire in one hand, red fire in the other. Child stage, 1 block tall.

Front is -z, y is up. Built by _impmon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _impmon import make

HEIGHT = 45
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "a long-limbed purple imp in a tall wizard hat with an X visor, a tattered red cape and blue and red fire in its hands"
build = make("impmonxantibody", x=True)
