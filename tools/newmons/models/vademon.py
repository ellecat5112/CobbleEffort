"""Vademon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a space alien with an enormous wrinkled pink brain for a head, goggling yellow eyes, a
long scrawny orange body, a silver ray gun and a skirt of green-tipped tentacles. 25 blocks.

Front is -z, y is up. Perfect stage. Built by _vademon.make.
"""
from __future__ import annotations

from _digi import sized
from _vademon import make

HEIGHT = 49
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a space alien with a huge pink brain head, goggling eyes, a scrawny orange body, a ray gun and tentacle legs"
build = make("vademon", False)
