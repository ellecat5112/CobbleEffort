"""Kyubimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the nine-tailed fox: a slender golden fox with a white chest ruff, a red-and-white rope collar with golden bells and nine golden tails wreathed in blue foxfire.
15 blocks long. Built by _kyubimon.make(silver=False).

Front is -z, y is up. 32 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _kyubimon import make

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
LOOK = "a slender golden fox with a white chest ruff, a red-and-white rope collar with golden bells and nine golden tails wreathed in blue foxfire"
build = make("kyubimon", silver=False)
