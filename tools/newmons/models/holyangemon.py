"""Holy Angemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the archangel: a tall angel warrior in grey plate under a white tabard, a violet-visored helm, eight
great white wings, a long violet sash and an Excalibur beam blade on its golden arm guard. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built by _holyangemon.make(priest=False).
"""
from __future__ import annotations

from _digi import sized
from _holyangemon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall angel warrior in grey plate and a white tabard with a visored helm, eight white wings and a beam blade"
build = make("holyangemon", priest=False)
