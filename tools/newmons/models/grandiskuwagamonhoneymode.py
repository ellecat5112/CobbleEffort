"""Grandis Kuwagamon Honey Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): Grandis Kuwagamon in Honey Mode, its armour black and yellow-gold, with four orange blade-wings in an X behind it. 35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage. Built by _kuwaga.make(look="honey").
"""
from __future__ import annotations

from _digi import sized
from _kuwaga import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Grandis Kuwagamon in Honey Mode, its armour black and yellow-gold, with four orange blade-wings in an X behind it"
build = make("grandiskuwagamonhoneymode", "honey")
