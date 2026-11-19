"""Vademon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Vademon changed by the X-Antibody: a grey-green alien in a black vest under a mottled khaki
brain, with an ear ring, a silver ray gun and a purple-tipped tentacle skirt. 25 blocks.

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
LOOK = "a grey-green space alien in a black vest under a khaki brain, with a ray gun and tentacle legs"
build = make("vademonxantibody", True)
