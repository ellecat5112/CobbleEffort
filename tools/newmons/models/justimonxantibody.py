"""Justimon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Justimon awakened by the X-Antibody: red armour with cyan lights, a white scarf, a
piston fist and a giant red X-marked arm cannon blazing blue. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _justimon.make(arm="accel", x=True).
"""
from __future__ import annotations

from _digi import sized
from _justimon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a masked red-armoured cyborg hero with a white scarf, a piston fist and a giant X-marked arm cannon"
build = make("justimonxantibody", arm="accel", x=True)
