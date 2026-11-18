"""Holy Angemon: Priest Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): Holy Angemon as a priest: long flowing white robes with a high collar, long blond
hair under the helm, eight white wings held round it and a long sword planted before it. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built by _holyangemon.make(priest=True).
"""
from __future__ import annotations

from _digi import sized
from _holyangemon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall angel in long flowing white robes with blond hair, eight white wings and a sword planted before it"
build = make("holyangemonpriestmode", priest=True)
