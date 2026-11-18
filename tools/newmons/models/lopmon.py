"""Lopmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a small round brown rabbit with a pink belly, dot eyes, a tiny horn and two huge long pink-striped ears that sweep out like wings and end in pink fingers.
Child stage, 1 block tall. Built by _lopmon.make(x=False).

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

from _digi import sized
from _lopmon import make

HEIGHT = 18
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a small round brown rabbit with a pink belly, dot eyes, a tiny horn and two huge long pink-striped ears that sweep out like wings and end in pink fingers"
build = make("lopmon", x=False)
