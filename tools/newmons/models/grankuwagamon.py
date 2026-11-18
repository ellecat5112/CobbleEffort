"""Gran Kuwagamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the stag-beetle beast: a long black-and-silver beetle with jagged mandibles, red eyes, four pink translucent wings and six bladed legs. 35 blocks tall.

Front is -z, y is up. 30 units tall; Ultimate stage. Built by _kuwaga.make(look="gran").
"""
from __future__ import annotations

from _digi import sized
from _kuwaga import make

HEIGHT = 30
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the stag-beetle beast: a long black-and-silver beetle with jagged mandibles, red eyes, four pink translucent wings and six bladed legs"
build = make("grankuwagamon", "gran")
