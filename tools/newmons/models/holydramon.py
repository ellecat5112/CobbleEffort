"""Holydramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the holy dragon, one of the Four Great Dragons: a long pink serpentine dragon with soft white fur
ruffs, a pale mane, long black horns banded magenta, small clawed arms and great pink wings. 35 blocks tall.

Front is -z, y is up. 50 units tall; Ultimate stage. Built by _holydramon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _holydramon import make

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "floater"
K = 3
LOOK = "a long pink serpentine holy dragon with white fur ruffs, banded black horns and great pink wings"
build = make("holydramon", x=False)
