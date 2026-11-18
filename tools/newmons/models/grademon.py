"""Grademon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the swordsman knight: lean gold armour with red details, a long-horned helm, ridged pauldrons, a
great deep blue cape, a green scabbard and two long thin swords. 25 blocks tall.

Front is -z, y is up. 76 units tall (the horns); Perfect stage. Built by _grademon.make(vice=False).
"""
from __future__ import annotations

from _digi import sized
from _grademon import make

HEIGHT = 76
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean gold-armoured swordsman knight with a long-horned helm, a deep blue cape and two long thin swords"
build = make("grademon", vice=False)
