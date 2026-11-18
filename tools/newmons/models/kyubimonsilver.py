"""Kyubimon (Silver) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a silver Kyubimon: grey-white fur, a red-and-white rope collar with golden bells and nine silver tails wreathed in red-orange flames.
15 blocks long. Built by _kyubimon.make(silver=True).

Front is -z, y is up. 32 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _kyubimon import make

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
LOOK = "a silver nine-tailed fox with grey-white fur, a red-and-white rope collar with golden bells and nine silver tails wreathed in red-orange flames"
build = make("kyubimonsilver", silver=True)
