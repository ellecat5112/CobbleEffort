"""Pegasmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Pegasmon changed by the X-Antibody: sleek crystalline gold armour seamed with glowing cyan and wings of gold and cyan light-blades. 15 blocks long.

Front is -z, y is up. 40 units tall; Adult (Armor) stage. Built by _pegasmon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _pegasmon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "Pegasmon changed by the X-Antibody: sleek crystalline gold armour seamed with glowing cyan and wings of gold and cyan light-blades"
build = make("pegasmonxantibody", x=True)
