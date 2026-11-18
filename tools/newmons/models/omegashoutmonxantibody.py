"""Omega Shoutmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Omega Shoutmon changed by the X-Antibody: heavier black-and-gold plate, bigger horns, a golden lance-blade and wings of fire. 25 blocks tall.

Front is -z, y is up. 72 units tall (the horns); Perfect stage. Built by _omegashoutmon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _omegashoutmon import make

HEIGHT = 72
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Omega Shoutmon changed by the X-Antibody: heavier black-and-gold plate, bigger horns, a golden lance-blade and wings of fire"
build = make("omegashoutmonxantibody", x=True)
