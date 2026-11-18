"""Mugendramon: MFS-3 Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Mugendramon refitted in black-and-chrome armour with skull-faced shoulder and knee plates, a huge drill-cone arm, two back cannons and a long rail-gun barrel. 35 blocks tall.

Front is -z, y is up. 72 units tall (the cannons); Ultimate stage. Built by _mugendramon.make(mfs3=True).
"""
from __future__ import annotations

from _digi import sized
from _mugendramon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "Mugendramon refitted in black-and-chrome armour with skull-faced shoulder and knee plates, a huge drill-cone arm, two back cannons and a long rail-gun barrel"
build = make("mugendramonmfs3mode", mfs3=True)
