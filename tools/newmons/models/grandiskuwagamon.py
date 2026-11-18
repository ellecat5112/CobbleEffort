"""Grandis Kuwagamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the armoured stag-beetle titan standing upright in black-and-silver plate, two huge glowing blade-mandibles crossed in an X behind it, red eyes and long claws. 35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage. Built by _kuwaga.make(look="grandis").
"""
from __future__ import annotations

from _digi import sized
from _kuwaga import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the armoured stag-beetle titan standing upright in black-and-silver plate, two huge glowing blade-mandibles crossed in an X behind it, red eyes and long claws"
build = make("grandiskuwagamon", "grandis")
