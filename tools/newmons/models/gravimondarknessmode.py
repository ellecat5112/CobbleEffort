"""Gravimon Darkness Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Gravimon in darkness: a lean figure in a red body suit with white armoured shoulders, great black and
gold wings crackling with orange lightning, a black flame crown and a curtain of cables with brass plugs hanging from
its outstretched white arms. 25 blocks tall.

Front is -z, y is up. 66 units tall; Perfect stage. Built by _gravimon.make(dark=True).
"""
from __future__ import annotations

from _digi import sized
from _gravimon import make

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a lean red-suited figure with white shoulders, black and gold lightning wings and a curtain of cables from its outstretched arms"
build = make("gravimondarknessmode", dark=True)
