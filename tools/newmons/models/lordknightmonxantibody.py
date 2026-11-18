"""Lord Knightmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Lord Knightmon awakened by the X-Antibody: a rose-pink armoured knight with a crimson rose-shaped shield, a long rapier and great fanned wings of golden blade-feathers with cyan crystal tips. 35 blocks tall. Built by _lordknightmon.make(x=True).

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _lordknightmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a rose-pink armoured knight with a crimson rose-shaped shield, a long rapier and great fanned wings of golden blade-feathers with cyan crystal tips"
build = make("lordknightmonxantibody", x=True)
