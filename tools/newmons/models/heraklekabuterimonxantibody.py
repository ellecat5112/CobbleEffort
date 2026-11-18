"""Herakle Kabuterimon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail
standard after the official art on wikimon.net): Herakle Kabuterimon awakened by the X-Antibody: bright gold armour,
red-orange wings, four clawed arms and a radiant golden orb held high. 35 blocks tall.

Front is -z, y is up. 78 units tall (the horn); Ultimate stage. Built by _herakle.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _herakle import make

HEIGHT = 78
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a towering bright gold Hercules beetle with a great curved horn, red-orange wings, four arms and a golden orb"
build = make("heraklekabuterimonxantibody", x=True)
