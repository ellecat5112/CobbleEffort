"""Nefertimon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Nefertimon changed by the X-Antibody: bronze-and-black armour, a jackal-eared golden headdress, black claws, great white wings and a blue-tufted tail. 15 blocks long.

Front is -z, y is up. 36 units tall; Adult (Armor) stage. Built by _nefertimon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _nefertimon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "Nefertimon changed by the X-Antibody: bronze-and-black armour, a jackal-eared golden headdress, black claws, great white wings and a blue-tufted tail"
build = make("nefertimonxantibody", x=True)
