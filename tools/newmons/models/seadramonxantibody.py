"""Seadramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a deep-blue sea serpent with flowing red streaks and fins, a huge golden finned head-crest and a purple-lipped toothy maw.
15 blocks. Built by _seadramon.make(x=True).

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _seadramon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a deep-blue sea serpent with flowing red streaks and fins, a huge golden finned head-crest and a purple-lipped toothy maw"
build = make("seadramonxantibody", x=True)
