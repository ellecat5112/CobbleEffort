"""Mammon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the armoured mammoth: a huge shaggy brown mammoth with a steel-plated head and trunk engraved with gold, a single glaring eye, long curved ivory tusks, a black spiked crest and pale wing-fins. 25 blocks long. Built by _mammon.make(x=False).

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _mammon import make

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
LOOK = "a huge shaggy brown mammoth with a steel-plated head and trunk engraved with gold, a single glaring eye, long curved ivory tusks, a black spiked crest and pale wing-fins"
build = make("mammon", x=False)
